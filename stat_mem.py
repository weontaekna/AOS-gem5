#!/usr/bin/env python2

#SCHEME = "AOS"
#OUTPUT_DIR="./output"
#OUTPUT_DIR="./bak_output/output-AOS-3b-old"
OUTPUT_DIR="./output-AOS-PARTS2"

#SCHEME = "UnsafeBaseline"
#OUTPUT_DIR="./output-inst"

#STATS = [
#"sim_seconds",
#"system.cpu.iew.mcq.thread0.cacheBlocked",
#"system.cpu.commit.committedPacma",
#"system.cpu.commit.committedXpacm",
#"system.cpu.iew.mcq.thread0.committedBndclr",
#"system.cpu.iew.mcq.thread0.committedBndstr",
#"system.cpu.iew.mcq.thread0.committedInsts",
#"system.cpu.iew.mcq.thread0.committedSignedLoad",
#"system.cpu.iew.mcq.thread0.committedSignedStore",
#"system.cpu.iew.mcq.thread0.committedUnsignedLoad",
#"system.cpu.iew.mcq.thread0.committedUnsignedStore",
#"system.cpu.iew.mcq.thread0.numBoundCheck",
#"system.cpu.iew.mcq.thread0.numCounterInc",
#"system.cpu.iew.mcq.thread0.numDataForwardedBoundCheck",
##"system.cpu.iew.mcq.thread0.numDataForwardedOccupancyCheck",
#"system.cpu.iew.mcq.thread0.numOccupancyCheck",
#"system.cpu.iew.mcq.thread0.numReplayedBoundCheck",
#"system.cpu.iew.mcq.thread0.numReplayedBoundStore",
#]

STATS = [
"system.ruby.network.routers.msg_bytes.BndLoad_Control::0",
"system.ruby.network.routers.msg_bytes.BndLoad_Control::1",
"system.ruby.network.routers.msg_bytes.BndLoad_Control::2",
"system.ruby.network.routers.msg_bytes.BndLoad_Data::0",
"system.ruby.network.routers.msg_bytes.BndLoad_Data::1",
"system.ruby.network.routers.msg_bytes.BndLoad_Data::2",
"system.ruby.network.routers.msg_bytes.BndStore_Control::0",
"system.ruby.network.routers.msg_bytes.BndStore_Control::1",
"system.ruby.network.routers.msg_bytes.BndStore_Control::2",
"system.ruby.network.routers.msg_bytes.BndStore_Data::0",
"system.ruby.network.routers.msg_bytes.BndStore_Data::1",
"system.ruby.network.routers.msg_bytes.BndStore_Data::2",
"system.ruby.network.routers.msg_bytes.Control::0",
"system.ruby.network.routers.msg_bytes.Control::1",
"system.ruby.network.routers.msg_bytes.Control::2",
"system.ruby.network.routers.msg_bytes.Request_Control::0",
"system.ruby.network.routers.msg_bytes.Request_Control::1",
"system.ruby.network.routers.msg_bytes.Request_Control::2",
"system.ruby.network.routers.msg_bytes.Request_Data::0",
"system.ruby.network.routers.msg_bytes.Request_Data::1",
"system.ruby.network.routers.msg_bytes.Request_Data::2",
"system.ruby.network.routers.msg_bytes.Response_Control::0",
"system.ruby.network.routers.msg_bytes.Response_Control::1",
"system.ruby.network.routers.msg_bytes.Response_Control::2",
"system.ruby.network.routers.msg_bytes.Response_Data::0",
"system.ruby.network.routers.msg_bytes.Response_Data::1",
"system.ruby.network.routers.msg_bytes.Response_Data::2",
"system.ruby.network.routers.msg_bytes.Writeback_Control::0",
"system.ruby.network.routers.msg_bytes.Writeback_Control::1",
"system.ruby.network.routers.msg_bytes.Writeback_Control::2",
"system.ruby.network.routers.msg_bytes.Writeback_Data::0",
"system.ruby.network.routers.msg_bytes.Writeback_Data::1",
"system.ruby.network.routers.msg_bytes.Writeback_Data::2",
]


SPEC = [
    "bzip2",
    "gcc",
    "mcf",
    "milc",
    "namd",
    "gobmk",
    "soplex",
    "povray",
    "hmmer",
    "sjeng",
    "libquantum",
    "h264ref",
    "lbm",
    "omnetpp",
    "astar",
    "sphinx3",
]

PARSEC = [
    "blackscholes",
    "bodytrack",
    "facesim",
    "ferret",
    "freqmine",
    "swaptions",
    "canneal",
    "fluidanimate",
    "streamcluster",
]

if __name__ == '__main__':
    fs = open("./stat_mem.txt", "w+")
    
    fs.write("=== SPEC Benchmarks ===\n")

    bench = SPEC

    for a in bench:
        fn = OUTPUT_DIR + "/SPEC-" + a + "/stats.txt"

        #fs.write("\n---network_traffic ---\n")
        sum = 0

        chk = 0
        for stat in STATS:
            try:
                fo = open(fn, "r")
            except:
                fs.write('%13s: ' % a)
                fs.write('\n')
                continue

            lines = fo.readlines()

            for line in lines:
                sline = [x for x in line.split(" ") if x]
                if stat == sline[0]:
                    chk = 1
                    #fs.write('%13s: ' % a)
                    #fs.write('%s\n' % sline[1])
                    sum += int(sline[1])
                    #break
            fo.close()


        if chk == 0:
            #fs.write('%13s: ' % a)
            fs.write('\n')
        else:
            fs.write(str(sum)+'\n')


