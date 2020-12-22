#ifndef __CPU_O3_MCQ_IMPL_HH__
#define __CPU_O3_MCQ_IMPL_HH__

#include <algorithm>
#include <list>
#include <string>

#include "base/logging.hh"
#include "cpu/o3/mcq.hh"
#include "debug/Drain.hh"
#include "debug/Fetch.hh"
#include "debug/MCQ.hh"
#include "debug/Writeback.hh"
#include "params/DerivO3CPU.hh"

using namespace std;

template <class Impl>
MCQ<Impl>::MCQ(O3CPU *cpu_ptr, IEW *iew_ptr, DerivO3CPUParams *params)
    : cpu(cpu_ptr), iewStage(iew_ptr),
      _cacheBlocked(false),
      cacheStorePorts(params->cacheStorePorts), usedStorePorts(0),
      cacheLoadPorts(params->cacheLoadPorts), usedLoadPorts(0),
      lsqPolicy(params->smtLSQPolicy),
      MCQEntries(params->MCQEntries),
      maxMCQEntries(maxMCQAllocation(lsqPolicy, MCQEntries, params->numThreads,
                  params->smtLSQThreshold)),
      numThreads(params->numThreads)
{
    assert(numThreads > 0 && numThreads <= Impl::MaxThreads);

    if (lsqPolicy == SMTQueuePolicy::Dynamic) {
        DPRINTF(MCQ, "MCQ sharing policy set to Dynamic\n");
    } else if (lsqPolicy == SMTQueuePolicy::Partitioned) {
        DPRINTF(Fetch, "MCQ sharing policy set to Partitioned: "
                "%i entries per MCQ\n", maxMCQEntries);
    } else if (lsqPolicy == SMTQueuePolicy::Threshold) {

        assert(params->smtLSQThreshold > params->MCQEntries);

        DPRINTF(MCQ, "MCQ sharing policy set to Threshold: "
                "%i entries per MCQ\n", maxMCQEntries);
    } else {
        panic("Invalid MCQ sharing policy. Options are: Dynamic, "
                    "Partitioned, Threshold");
    }

    isBtAllocated = false;
    btBaseAddr = 0x1FFF00000000;

    const std::string scheme = params->simulateScheme;

    if (scheme.compare("UnsafeBaseline") == 0 || scheme.compare("PA") == 0) {
        needBtAllocated = false;
    } else if (scheme.compare("AOS") == 0) {
        needBtAllocated = true;
    } else {
        assert(false && "Wrong simulate Scheme\n");
    }

    btNumWays = params->btNumWays;
    int W = 16; // Default: 16, width of PAC
    //int S = log2(16); // 2 * 8B, size of bounds
    int S = log2(8); // 2 * 8B, size of bounds
    int N = log2(btNumWays) + 2;

    btSize = (uint64_t) (1 << (W + S + N));

    thread.reserve(numThreads);
    for (ThreadID tid = 0; tid < numThreads; tid++) {
        thread.emplace_back(MCQEntries, params->BIBEntries);
        thread[tid].init(cpu, iew_ptr, params, this, tid);
        thread[tid].setDcachePort(&cpu_ptr->getDataPort());
    }
}

template<class Impl>
std::string
MCQ<Impl>::name() const
{
    return iewStage->name() + ".mcq";
}

template<class Impl>
void
MCQ<Impl>::regStats()
{
    //Initialize MCQs
    for (ThreadID tid = 0; tid < numThreads; tid++) {
        thread[tid].regStats();
    }
}

template<class Impl>
void
MCQ<Impl>::setActiveThreads(list<ThreadID> *at_ptr)
{
    activeThreads = at_ptr;
    assert(activeThreads != 0);
}

template <class Impl>
void
MCQ<Impl>::drainSanityCheck() const
{
    assert(isDrained());

    for (ThreadID tid = 0; tid < numThreads; tid++)
        thread[tid].drainSanityCheck();
}

template <class Impl>
bool
MCQ<Impl>::isDrained() const
{
    bool drained(true);

    if (!isEmpty()) {
        DPRINTF(Drain, "Not drained, MCQ not empty.\n");
        drained = false;
    }

    return drained;
}

template <class Impl>
void
MCQ<Impl>::takeOverFrom()
{
    usedStorePorts = 0;
    _cacheBlocked = false;

    for (ThreadID tid = 0; tid < numThreads; tid++) {
        thread[tid].takeOverFrom();
    }
}

template <class Impl>
void
MCQ<Impl>::tick()
{
    if (needBtAllocated && !isBtAllocated) {
        list<ThreadID>::iterator threads = activeThreads->begin();
        list<ThreadID>::iterator end = activeThreads->end();

        while (threads != end) {
            ThreadID tid = *threads++;

            cpu->thread[tid]->getProcessPtr()->allocateMem(btBaseAddr, btSize);
        }

        printf("[AOS] Bound table is allocated! btSize: %lu btNumWays: %d\n",
                btSize, btNumWays);

        isBtAllocated = true;
    }

    usedLoadPorts = 0;
    usedStorePorts = 0;
}

template<class Impl>
void
MCQ<Impl>::cacheUnblocked()
{
    cacheBlocked(false);

    list<ThreadID>::iterator threads = activeThreads->begin();
    list<ThreadID>::iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;
        thread[tid].cacheUnblocked();
    }
}

template<class Impl>
bool
MCQ<Impl>::cacheBlocked() const
{
    return _cacheBlocked;
}

template<class Impl>
void
MCQ<Impl>::cacheBlocked(bool v)
{
    _cacheBlocked = v;
}

template<class Impl>
bool
MCQ<Impl>::cachePortAvailable(bool is_load) const
{
    bool ret;

    if (is_load) {
        ret  = usedLoadPorts < cacheLoadPorts;
    } else {
        ret  = usedStorePorts < cacheStorePorts;
    }

    return ret;
}

template<class Impl>
void
MCQ<Impl>::cachePortBusy(bool is_load)
{
    assert(cachePortAvailable(is_load));

    if (is_load) {
        usedLoadPorts++;
    } else {
        usedStorePorts++;
    }
}

template<class Impl>
void
MCQ<Impl>::insertInst(const DynInstPtr &inst)
{
    ThreadID tid = inst->threadNumber;

    thread[tid].insertInst(inst);
}

template <class Impl>
void
MCQ<Impl>::execute()
{
    for (ThreadID tid = 0; tid < numThreads; tid++) {
        thread[tid].execute();
    }
}

template<class Impl>
void
MCQ<Impl>::writebackStores()
{
    list<ThreadID>::iterator threads = activeThreads->begin();
    list<ThreadID>::iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;

        thread[tid].writebackStores();
    }
}

template <class Impl>
void
MCQ<Impl>::recvReqRetry()
{
    iewStage->cacheUnblocked();
    cacheBlocked(false);

    for (ThreadID tid : *activeThreads) {
        thread[tid].recvRetry();
    }
}

template <class Impl>
void
MCQ<Impl>::completeDataAccess(PacketPtr pkt)
{
    auto senderState = dynamic_cast<MCQSenderState*>(pkt->senderState);
    thread[cpu->contextToThread(senderState->contextId())]
        .completeDataAccess(pkt);
}

template <class Impl>
bool
MCQ<Impl>::recvTimingResp(PacketPtr pkt)
{
    if (pkt->isError())
        DPRINTF(MCQ, "Got error packet back for address: %#X\n",
                pkt->getAddr());

    assert(pkt->senderState); //yh+

    auto senderState = dynamic_cast<MCQSenderState*>(pkt->senderState);
    panic_if(!senderState, "Got packet back with unknown sender state\n");

    thread[cpu->contextToThread(senderState->contextId())].recvTimingResp(pkt);

    if (pkt->isInvalidate()) {
        assert(false && "pkt->isInvalidate()\n");
        // This response also contains an invalidate; e.g. this can be the case
        // if cmd is ReadRespWithInvalidate.
        //
        // The calling order between completeDataAccess and checkSnoop matters.
        // By calling checkSnoop after completeDataAccess, we ensure that the
        // fault set by checkSnoop is not lost. Calling writeback (more
        // specifically inst->completeAcc) in completeDataAccess overwrites
        // fault, and in case this instruction requires squashing (as
        // determined by checkSnoop), the ReExec fault set by checkSnoop would
        // be lost otherwise.

        DPRINTF(MCQ, "received invalidation with response for addr:%#x\n",
                pkt->getAddr());

        for (ThreadID tid = 0; tid < numThreads; tid++) {
            thread[tid].checkSnoop(pkt);
        }
    }
    //// Update the MCQRequest state (this may delete the request)
    senderState->request()->packetReplied();

    return true;
}

template <class Impl>
void
MCQ<Impl>::recvTimingSnoopReq(PacketPtr pkt)
{
    assert(false && "Snoop never occcurs\n"); //yh= TODO

    DPRINTF(MCQ, "received pkt for addr:%#x %s\n", pkt->getAddr(),
            pkt->cmdString());

    // must be a snoop
    if (pkt->isInvalidate()) {
        DPRINTF(MCQ, "received invalidation for addr:%#x\n",
                pkt->getAddr());
        for (ThreadID tid = 0; tid < numThreads; tid++) {
            thread[tid].checkSnoop(pkt);
        }
    }
}

template<class Impl>
int
MCQ<Impl>::getCount()
{
    unsigned total = 0;

    list<ThreadID>::iterator threads = activeThreads->begin();
    list<ThreadID>::iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;

        total += getCount(tid);
    }

    return total;
}

template<class Impl>
int
MCQ<Impl>::numInsts()
{
    unsigned total = 0;

    list<ThreadID>::iterator threads = activeThreads->begin();
    list<ThreadID>::iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;

        total += numInsts(tid);
    }

    return total;
}

template<class Impl>
unsigned
MCQ<Impl>::numFreeEntries()
{
    unsigned total = 0;

    list<ThreadID>::iterator threads = activeThreads->begin();
    list<ThreadID>::iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;

        total += thread[tid].numFreeEntries();
    }

    return total;
}

template<class Impl>
unsigned
MCQ<Impl>::numFreeEntries(ThreadID tid)
{
        return thread[tid].numFreeEntries();
}

template<class Impl>
bool
MCQ<Impl>::isFull()
{
    list<ThreadID>::iterator threads = activeThreads->begin();
    list<ThreadID>::iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;

        if (!thread[tid].isFull())
            return false;
    }

    return true;
}

template<class Impl>
bool
MCQ<Impl>::isFull(ThreadID tid)
{
    return thread[tid].isFull();
}

template<class Impl>
bool
MCQ<Impl>::isEmpty() const
{
    list<ThreadID>::const_iterator threads = activeThreads->begin();
    list<ThreadID>::const_iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;

        if (!thread[tid].isEmpty())
            return false;
    }

    return true;
}

template<class Impl>
void
MCQ<Impl>::dumpInsts() const
{
    list<ThreadID>::const_iterator threads = activeThreads->begin();
    list<ThreadID>::const_iterator end = activeThreads->end();

    while (threads != end) {
        ThreadID tid = *threads++;

        thread[tid].dumpInsts();
    }
}

static Addr
addrBlockOffset(Addr addr, unsigned int block_size)
{
    return addr & (block_size - 1);
}

static Addr
addrBlockAlign(Addr addr, uint64_t block_size)
{
    return addr & ~(block_size - 1);
}

static bool
transferNeedsBurst(Addr addr, uint64_t size, uint64_t block_size)
{
    return (addrBlockOffset(addr, block_size) + size) > block_size;
}

template<class Impl>
Fault
MCQ<Impl>::pushRequest(const DynInstPtr& inst, bool isLoad, uint8_t *data,
                       unsigned int size, Addr addr, Request::Flags flags,
                       uint64_t *res, AtomicOpFunctor *amo_op)
{
    ThreadID tid = cpu->contextToThread(inst->contextId());
    auto cacheLineSize = cpu->cacheLineSize();
    bool needs_burst = transferNeedsBurst(addr, size, cacheLineSize);
    MCQRequest* req = thread[tid].mchkQueue[inst->mcqIdx].request();

    assert(!needs_burst && "SplitDataRequest is required!\n");

    assert(!req);

    if (needs_burst) {
        assert(false);
        req = new SplitDataRequest(&thread[tid], inst, isLoad, addr,
                size, flags, data, res);
    } else {
        req = new SingleDataRequest(&thread[tid], inst, isLoad, addr,
                size, flags, data, res, nullptr);
    }

    assert(req);
    inst->setRequest(); // Mark ReqMade flag
    thread[tid].mchkQueue[inst->mcqIdx].req = req; //yh+
    req->taskId(cpu->taskId());

    req->initiateTranslation();

    assert(req->isTranslationComplete() && "!req->isTranslationComplete()\n");

    if (inst->getFault() == NoFault) {
        if (isLoad) {
            assert(isLoad);
            cpu->check(req, inst->mcqIdx);
        }
    }

    return inst->getFault();
}

template<class Impl>
void
MCQ<Impl>::SingleDataRequest::finish(const Fault &fault, const RequestPtr &req,
        ThreadContext* tc, BaseTLB::Mode mode)
{
    _fault.push_back(fault);
    numInTranslationFragments = 0;
    numTranslatedFragments = 1;
    /* If the instruction has been squahsed, let the request know
     * as it may have to self-destruct. */
    if (_inst->isSquashed()) {
        this->squashTranslation();
    } else {
        _inst->strictlyOrdered(req->isStrictlyOrdered());

        flags.set(Flag::TranslationFinished);
        if (fault == NoFault) {
            _inst->physEffAddr = req->getPaddr();
            _inst->memReqFlags = req->getFlags();
            if (req->isCondSwap()) {
                assert(_res);
                req->setExtraData(*_res);
            }
            setState(State::Request);
        } else {
            setState(State::Fault);
        }

        MCQRequest::_inst->fault = fault;
        MCQRequest::_inst->translationCompleted(true);
    }
}

template<class Impl>
void
MCQ<Impl>::SplitDataRequest::finish(const Fault &fault, const RequestPtr &req,
        ThreadContext* tc, BaseTLB::Mode mode)
{
    _fault.push_back(fault);
    assert(req == _requests[numTranslatedFragments] || this->isDelayed());

    numInTranslationFragments--;
    numTranslatedFragments++;

    mainReq->setFlags(req->getFlags());

    if (numTranslatedFragments == _requests.size()) {
        if (_inst->isSquashed()) {
            this->squashTranslation();
        } else {
            _inst->strictlyOrdered(mainReq->isStrictlyOrdered());
            flags.set(Flag::TranslationFinished);
            auto fault_it = _fault.begin();
            /* Ffwd to the first NoFault. */
            while (fault_it != _fault.end() && *fault_it == NoFault)
                fault_it++;
            /* If none of the fragments faulted: */
            if (fault_it == _fault.end()) {
                _inst->physEffAddr = request(0)->getPaddr();

                _inst->memReqFlags = mainReq->getFlags();
                if (mainReq->isCondSwap()) {
                    assert(_res);
                    mainReq->setExtraData(*_res);
                }
                setState(State::Request);
                _inst->fault = NoFault;
            } else {
                setState(State::Fault);
                _inst->fault = *fault_it;
            }
            _inst->translationCompleted(true);
        }
    }
}

template<class Impl>
void
MCQ<Impl>::SingleDataRequest::initiateTranslation()
{
    _inst->translationStarted(true);
    setState(State::Translation);
    flags.set(Flag::TranslationStarted);

    //_inst->savedReq = this;
    sendFragmentToTranslation(0);

    if (isTranslationComplete()) {
    }
}

template<class Impl>
PacketPtr
MCQ<Impl>::SplitDataRequest::mainPacket()
{
    return _mainPacket;
}

template<class Impl>
RequestPtr
MCQ<Impl>::SplitDataRequest::mainRequest()
{
    return mainReq;
}

template<class Impl>
void
MCQ<Impl>::SplitDataRequest::initiateTranslation()
{
    _inst->translationStarted(true);
    setState(State::Translation);
    flags.set(Flag::TranslationStarted);

    unsigned int cacheLineSize = _port.cacheLineSize();
    Addr base_addr = _addr;
    Addr next_addr = addrBlockAlign(_addr + cacheLineSize, cacheLineSize);
    Addr final_addr = addrBlockAlign(_addr + _size, cacheLineSize);
    uint32_t size_so_far = 0;

    mainReq = std::make_shared<Request>(_inst->getASID(), base_addr,
                _size, _flags, _inst->masterId(),
                _inst->instAddr(), _inst->contextId());

    // Paddr is not used in mainReq. However, we will accumulate the flags
    // from the sub requests into mainReq by calling setFlags() in finish().
    // setFlags() assumes that paddr is set so flip the paddr valid bit here to
    // avoid a potential assert in setFlags() when we call it from  finish().
    mainReq->setPaddr(0);

    /* Get the pre-fix, possibly unaligned. */
    _requests.push_back(std::make_shared<Request>(_inst->getASID(), base_addr,
                next_addr - base_addr, _flags, _inst->masterId(),
                _inst->instAddr(), _inst->contextId()));
    size_so_far = next_addr - base_addr;

    /* We are block aligned now, reading whole blocks. */
    base_addr = next_addr;
    while (base_addr != final_addr) {
        _requests.push_back(std::make_shared<Request>(_inst->getASID(),
                    base_addr, cacheLineSize, _flags, _inst->masterId(),
                    _inst->instAddr(), _inst->contextId()));
        size_so_far += cacheLineSize;
        base_addr += cacheLineSize;
    }

    /* Deal with the tail. */
    if (size_so_far < _size) {
        _requests.push_back(std::make_shared<Request>(_inst->getASID(),
                    base_addr, _size - size_so_far, _flags, _inst->masterId(),
                    _inst->instAddr(), _inst->contextId()));
    }

    /* Setup the requests and send them to translation. */
    for (auto& r: _requests) {
        r->setReqInstSeqNum(_inst->seqNum);
        r->taskId(_taskId);
    }
    //this->_inst->savedReq = this;
    numInTranslationFragments = 0;
    numTranslatedFragments = 0;

    for (uint32_t i = 0; i < _requests.size(); i++) {
        sendFragmentToTranslation(i);
    }
}

template<class Impl>
void
MCQ<Impl>::MCQRequest::sendFragmentToTranslation(int i)
{
    numInTranslationFragments++;
    _port.dTLB()->translateTiming(
            this->request(i),
            this->_inst->thread->getTC(), this,
            this->isLoad() ? BaseTLB::Read : BaseTLB::Write);
}

template<class Impl>
bool
MCQ<Impl>::SingleDataRequest::recvTimingResp(PacketPtr pkt)
{
    assert(_numOutstandingPackets == 1);
    auto state = dynamic_cast<MCQSenderState*>(pkt->senderState);
    setState(State::Complete);
    flags.set(Flag::Complete);
    state->outstanding--;
    assert(pkt == _packets.front());

    _port.completeDataAccess(pkt);
    return true;
}

template<class Impl>
bool
MCQ<Impl>::SplitDataRequest::recvTimingResp(PacketPtr pkt)
{
    auto state = dynamic_cast<MCQSenderState*>(pkt->senderState);
    uint32_t pktIdx = 0;
    while (pktIdx < _packets.size() && pkt != _packets[pktIdx])
        pktIdx++;
    assert(pktIdx < _packets.size());
    assert(pkt->req == _requests[pktIdx]);
    assert(pkt == _packets[pktIdx]);
    numReceivedPackets++;
    state->outstanding--;
    if (numReceivedPackets == _packets.size()) {
        setState(State::Complete);
        flags.set(Flag::Complete);
        /* Assemble packets. */
        PacketPtr resp = isLoad()
            ? Packet::createRead(mainReq)
            : Packet::createWrite(mainReq);
        if (isLoad())
            resp->dataStatic(_inst->memData);
        else
            resp->dataStatic(_data);
        resp->senderState = _senderState;
        _port.completeDataAccess(resp);
        delete resp;
    }
    return true;
}

template<class Impl>
void
MCQ<Impl>::SingleDataRequest::buildPackets()
{
    assert(_senderState);
    /* Retries do not create new packets. */
    if (_packets.size() == 0) {
        _packets.push_back(
                isLoad()
                    ?  Packet::createRead(request())
                    :  Packet::createWrite(request()));
        _packets.back()->dataStatic(_inst->memData);
        _packets.back()->senderState = _senderState;

        assert(_packets.back()->senderState);
    }
    assert(_packets.size() == 1);
}

template<class Impl>
void
MCQ<Impl>::SplitDataRequest::buildPackets()
{
    /* Extra data?? */
    ptrdiff_t offset = 0;
    if (_packets.size() == 0) {
        /* New stuff */
        if (isLoad()) {
            _mainPacket = Packet::createRead(mainReq);
            _mainPacket->dataStatic(_inst->memData);
        }
        for (auto& r: _requests) {
            PacketPtr pkt = isLoad() ? Packet::createRead(r)
                                    : Packet::createWrite(r);
            if (isLoad()) {
                pkt->dataStatic(_inst->memData + offset);
            } else {
                uint8_t* req_data = new uint8_t[r->getSize()];
                std::memcpy(req_data,
                        _inst->memData + offset,
                        r->getSize());
                pkt->dataDynamic(req_data);
            }
            offset += r->getSize();
            pkt->senderState = _senderState;
            _packets.push_back(pkt);
        }
    }
    assert(_packets.size() == _requests.size());
}

template<class Impl>
void
MCQ<Impl>::SingleDataRequest::sendPacketToCache()
{
    assert(_numOutstandingPackets == 0);
    if (mcqUnit()->trySendPacket(isLoad(), _packets.at(0)))
        _numOutstandingPackets = 1;
}

template<class Impl>
void
MCQ<Impl>::SplitDataRequest::sendPacketToCache()
{
    /* Try to send the packets. */
    while (numReceivedPackets + _numOutstandingPackets < _packets.size() &&
            mcqUnit()->trySendPacket(isLoad(),
                _packets.at(numReceivedPackets + _numOutstandingPackets))) {
        _numOutstandingPackets++;
    }
}

template<class Impl>
bool
MCQ<Impl>::SingleDataRequest::isCacheBlockHit(Addr blockAddr, Addr blockMask)
{
    return ( (MCQRequest::_requests[0]->getPaddr() & blockMask) == blockAddr);
}

template<class Impl>
bool
MCQ<Impl>::SplitDataRequest::isCacheBlockHit(Addr blockAddr, Addr blockMask)
{
    bool is_hit = false;
    for (auto &r: _requests) {
        if ((r->getPaddr() & blockMask) == blockAddr) {
            is_hit = true;
            break;
        }
    }
    return is_hit;
}

#endif//__CPU_O3_MCQ_IMPL_HH__
