import m5
from m5.objects import *

x86_suffix = '_base.hparch_test-m64-wllvm'

#500.perlbench_r
perlbench_r = Process() # Update June 7, 2017: This used to be LiveProcess()
perlbench_r.executable =  'perlbench_r' + x86_suffix
# TEST CMDS
#perlbench_r.cmd = [perlbench_r.executable] + ['-I.', '-I./lib', 'attrs.pl']
# REF CMDS
perlbench_r.cmd = [perlbench_r.executable] + ['-I./lib', 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']
#perlbench_r.cmd = [perlbench_r.executable] + ['-I./lib', 'diffmail.pl', '4', '800', '10', '17', '19', '300']
#perlbench_r.cmd = [perlbench_r.executable] + ['-I./lib', 'splitmail.pl', '6400', '12', '26', '16', '100', '0']
#perlbench_r.output = out_dir+'perlbench.out'

#600.perlbench_s
perlbench_s = Process() # Update June 7, 2017: This used to be LiveProcess()
perlbench_s.executable =  'perlbench_s' + x86_suffix
# TEST CMDS
#perlbench_s.cmd = [perlbench_s.executable] + ['-I.', '-I./lib', 'attrs.pl']
# REF CMDS
perlbench_s.cmd = [perlbench_s.executable] + ['-I./lib', 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']
#perlbench_s.cmd = [perlbench_s.executable] + ['-I./lib', 'diffmail.pl', '4', '800', '10', '17', '19', '300']
#perlbench_s.cmd = [perlbench_s.executable] + ['-I./lib', 'splitmail.pl', '6400', '12', '26', '16', '100', '0']
#perlbench_s.output = out_dir+'perlbench.out'

#502.gcc_r
gcc_r = Process()
gcc_r.executable = 'cpugcc_r' + x86_suffix
# TEST CMDS
#gcc_r.cmd = [gcc_r.executable] + ['t1.c', '-O3', '-finline-limit=50000', '-o', 't1.opts-O3_-finline-limit_50000.s']
# REF CMDS
gcc_r.cmd = [gcc_r.executable] + ['gcc-pp.c', '-O3', '-finline-limit=0', '-fif-conversion', '-fif-conversion2', \
                                   '-o', 'gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.s']
#gcc_r.cmd = [gcc_r.executable] + ['gcc-pp.c', '-O2', '-finline-limit=36000', '-fpic', '-o', 'gcc-pp.opts-O2_-finline-limit_36000_-fpic.s']
#gcc_r.cmd = [gcc_r.executable] + ['gcc-smaller.c', 'O3', '-fipa-pta', '-o', 'gcc-smaller.opts-O3_-fipa-pta.s']
#gcc_r.cmd = [gcc_r.executable] + ['ref32.c', '-O5', '-o', 'ref32.opts-O5.s']
#gcc_r.cmd = [gcc_r.executable] + ['ref32.c', '-O3', '-fselective-scheduling', '-fselective-scheduling2', '-o', \
#                                  'ref32.opts-O3_-fselective-scheduling_-fselective-scheduling2.s']
#gcc_r.output = out_dir + 'gcc.out'

#602.gcc_s
gcc_s = Process()
gcc_s.executable = 'sgcc' + x86_suffix
# TEST CMDS
#gcc_s.cmd = [gcc_s.executable] + ['t1.c', '-O3', '-finline-limit=50000', '-o', 't1.opts-O3_-finline-limit_50000.s']
# REF CMDS
gcc_s.cmd = [gcc_s.executable] + ['gcc-pp.c', '-O5', '-fipa-pta', '-o', 'gcc-pp.opts-O5_-fipa-pta.s']
#gcc_s.cmd = [gcc_s.executable] + ['gcc-pp.c', '-O5', '-finline-limit=1000', '-fselective-scheduling', \
#                                  '-fselective-scheduling2', '-o', \
#                                  'gcc-pp.opts-O5_-finline-limit_1000_-fselective-scheduling_-fselective-scheduling2.s']
#gcc_s.cmd = [gcc_s.executable] + ['gcc-pp.c', '-O5', '-finline-limit=24000', '-fgcse', '-fgcse-las', '-fgcse-lm', \
#                                  '-fgcse-sm', '-o', 'gcc-pp.opts-O5_-finline-limit_24000_-fgcse_-fgcse-las_-fgcse-lm_-fgcse-sm.s']
#gcc_s.output = out_dir + 'gcc.out'

#505.mcf_r
mcf_r = Process()
mcf_r.executable = 'mcf_r' + x86_suffix
# TEST, TRAIN, REF CMDS
mcf_r.cmd = [mcf_r.executable] + ['inp.in']
#mcf_r.output = out_dir + 'mcf.out'

#605.mcf_s
mcf_s = Process()
mcf_s.executable = 'mcf_s' + x86_suffix
# TEST, TRAIN, REF CMDS
mcf_s.cmd = [mcf_s.executable] + ['inp.in']
#mcf_s.output = out_dir + 'mcf.out'

#520.omnetpp_r
omnetpp_r = Process()
omnetpp_r.executable = 'omnetpp_r' + x86_suffix
# TEST, TRAIN, REF CMDS
omnetpp_r.cmd = [omnetpp_r.executable] + ['-c', 'General', '-r', '0']
#omnetpp_r.output = out_dir + 'omnetpp.out'

#620.omnetpp_s
omnetpp_s = Process()
omnetpp_s.executable = 'omnetpp_s' + x86_suffix
# TEST, TRAIN, REF CMDS
omnetpp_s.cmd = [omnetpp_s.executable] + ['-c', 'General', '-r', '0']
#omnetpp_s.output = out_dir + 'omnetpp.out'


#523.xalancbmk_r
xalancbmk_r = Process()
xalancbmk_r.executable = 'cpuxalan_r' + x86_suffix
# TEST CMDS
#xalancbmk_r.cmd = [xalancbmk_r.executable] + ['-v', 'test.xml', 'xalanc.xsl']
# TRAIN CMDS
#xalancbmk_r.cmd = [xalancbmk_r.executable] + ['-v', 'allbooks.xml', 'xalanc.xsl']
# REF CMDS
xalancbmk_r.cmd = [xalancbmk_r.executable] + ['-v', 't5.xml','xalanc.xsl']
#xalancbmk_r.output = out_dir + 'xalancbmk.out'

#623.xalancbmk_s
xalancbmk_s = Process()
xalancbmk_s.executable = 'xalancbmk_s' + x86_suffix
# TEST CMDS
#xalancbmk_s.cmd = [xalancbmk_s.executable] + ['-v', 'test.xml', 'xalanc.xsl']
# TRAIN CMDS
#xalancbmk_s.cmd = [xalancbmk_s.executable] + ['-v', 'allbooks.xml', 'xalanc.xsl']
# REF CMDS
xalancbmk_s.cmd = [xalancbmk_s.executable] + ['-v', 't5.xml','xalanc.xsl']
#xalancbmk_s.output = out_dir + 'xalancbmk.out'


#525.x264_r
x264_r = Process()
x264_r.executable = 'ldecod_r' + x86_suffix
# TEST CMDS
#x264_r.cmd = [x264_r.executable] + ['--dumpyuv', '50', '--frames', '156', '-o', 'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
# TRAIN CMDS
#x264_r.cmd = [x264_r.executable] + ['--dumpyuv', '50', '--frames', '142', '-o', 'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
# REF CMDS
x264_r.cmd = [x264_r.executable] + ['-i', 'BuckBunny.264', '-o', 'BuckBunny.yuv']
# ['--pass', '1', '--stats', 'x264_stats.log', '--bitrate', '1000', '--frames', '1000', '-o', \
#                                'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
#x264_r.cmd = [x264_r.executable] + ['--pass', '2', '--stats', 'x264_stats.log', '--bitrate', '1000', '--dumpyuv', '200', \
#                                  '--frames', '1000', '-o', 'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
#x264_r.cmd = [x264_r.executable] + ['--seek', '500', '--dumpyuv', '200', '--frames', '1250', '-o', 'BuckBunny_New.264', \
#                                 'BuckBunny.yuv', '1280x720']
#x264_r.output = out_dir + 'x264.out'


#625.x264_s
x264_s = Process()
x264_s.executable = 'ldecod_s' + x86_suffix
# TEST CMDS
#x264_s.cmd = [x264_s.executable] + ['--dumpyuv', '50', '--frames', '156', '-o', 'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
# TRAIN CMDS
#x264_s.cmd = [x264_s.executable] + ['--dumpyuv', '50', '--frames', '142', '-o', 'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
# REF CMDS
x264_s.cmd = [x264_r.executable] + ['-i', 'BuckBunny.264', '-o', 'BuckBunny.yuv']
#x264_s.cmd = [x264_s.executable] + ['--pass', '1', '--stats', 'x264_stats.log', '--bitrate', '1000', '--frames', '1000', '-o', \
#                                'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
#x264_s.cmd = [x264_s.executable] + ['--pass', '2', '--stats', 'x264_stats.log', '--bitrate', '1000', '--dumpyuv', '200', \
#                                  '--frames', '1000', '-o', 'BuckBunny_New.264', 'BuckBunny.yuv', '1280x720']
#x264_s.cmd = [x264_s.executable] + ['--seek', '500', '--dumpyuv', '200', '--frames', '1250', '-o', 'BuckBunny_New.264', \
#                                 'BuckBunny.yuv', '1280x720']
#x264_s.output = out_dir + 'x264.out'


#531.deepsjeng_r
deepsjeng_r = Process()
deepsjeng_r.executable = 'deepsjeng_r' + x86_suffix
# TEST CMDS
#deepsjeng_r.cmd = [deepsjeng_r.executable] + ['test.txt']
# TRAIN CMDS
#deepsjeng_r.cmd = [deepsjeng_r.executable] + ['train.txt']
# REF CMDS
deepsjeng_r.cmd = [deepsjeng_r.executable] + ['ref.txt']

#631.deepsjeng_s
deepsjeng_s = Process()
deepsjeng_s.executable = 'deepsjeng_s' + x86_suffix
# TEST CMDS
#deepsjeng_s.cmd = [deepsjeng_s.executable] + ['test.txt']
# TRAIN CMDS
#deepsjeng_s.cmd = [deepsjeng_s.executable] + ['train.txt']
# REF CMDS
deepsjeng_s.cmd = [deepsjeng_s.executable] + ['ref.txt']

#541.leela_r
leela_r = Process()
leela_r.executable = 'leela_r' + x86_suffix
# TEST CMDS
#leela_r.cmd = [leela_r.executable] + ['test.sgf']
# TRAIN CMDS
#leela_r.cmd = [leela_r.executable] + ['train.sgf']
# REF CMDS
leela_r.cmd = [leela_r.executable] + ['ref.sgf']

#641.leela_s
leela_s = Process()
leela_s.executable = 'leela_s' + x86_suffix
# TEST CMDS
#leela_s.cmd = [leela_s.executable] + ['test.sgf']
# TRAIN CMDS
#leela_s.cmd = [leela_s.executable] + ['train.sgf']
# REF CMDS
leela_s.cmd = [leela_s.executable] + ['ref.sgf']

#548.exchange2_r
exchange2_r = Process()
exchange2_r.executable = 'exchange2_r' + x86_suffix
# TEST CMDS
#exchange2_r.cmd = [exchange2_r.executable] + ['0']
# TRAIN CMDS
#exchange2_r.cmd = [exchange2_r.executable] + ['1']
# REF CMDS
exchange2_r.cmd = [exchange2_r.executable] + ['6']

#648.exchange2_s
exchange2_s = Process()
exchange2_s.executable = 'exchange2_s' + x86_suffix
# TEST CMDS
#exchange2_s.cmd = [exchange2_s.executable] + ['0']
# TRAIN CMDS
#exchange2_s.cmd = [exchange2_s.executable] + ['1']
# REF CMDS
exchange2_s.cmd = [exchange2_s.executable] + ['6']

#557.xz_r
xz_r = Process()
xz_r.executable = 'xz_r' + x86_suffix
# TEST CMDS
#xz_r.cmd = [xz_r.executable] + ['cpu2006docs.tar.xz', '4', \
#       '055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae', \
#       '1548636', '1555348', '0']
# TRAIN CMDS
#xz_r.cmd = [xz_r.executable] + ['input.combined.xz', '40', \
#       'a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf', \
#       '6356684', '-1', '8']
# REF CMDS
xz_r.cmd = [xz_r.executable] + ['cld.tar.xz', '160', \
        '19cf30ae51eddcbefda78dd06014b4b96281456e078ca7c13e1c0c9e6aaea8dff3efb4ad6b0456697718cede6bd5454852652806a657bb56e07d61128434b474', \
        '59796407', '61004416', '6']
#xz_r.cmd = [xz_r.executable] + ['cpu2006docs.tar.xz', '250', \
#       '055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae', \
#       '23047774', '23513385', '6e']
#xz_r.cmd = [xz_r.executable] + ['input.combined.xz', '250', \
#       'a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf', \
#       '40401484', '41217675', '7']

#657.xz_s
xz_s = Process()
xz_s.executable = 'xz_s' + x86_suffix
# TEST CMDS
#xz_s.cmd = [xz_s.executable] + ['cpu2006docs.tar.xz', '4', \
#       '055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae', \
#       '1548636', '1555348', '0']
# TRAIN CMDS
#xz_s.cmd = [xz_s.executable] + ['input.combined.xz', '40', \
#       'a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf', \
#       '6356684', '-1', '8']
# REF CMDS
xz_s.cmd = [xz_s.executable] + ['cpu2006docs.tar.xz', '6643', \
        '055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae', \
        '1036078272', '1111795472', '4']
#xz_s.cmd = [xz_s.executable] + ['cld.tar.xz', '1400', \
#           '19cf30ae51eddcbefda78dd06014b4b96281456e078ca7c13e1c0c9e6aaea8dff3efb4ad6b0456697718cede6bd5454852652806a657bb56e07d61128434b474', \
#           '536995164', '539938872', '8']

#503.bwaves_r
bwaves_r = Process()
bwaves_r.executable = 'bwaves_r' + x86_suffix
# REF CMDS
bwaves_r.cmd = [bwaves_r.executable] + ['bwaves_1']
bwaves_r.input = 'bwaves_1.in'
#bwaves_r.output = out_dir + 'bwaves.out'

#603.bwaves_s
bwaves_s = Process()
bwaves_s.executable = 'speed_bwaves' + x86_suffix
# REF CMDS
bwaves_s.cmd = [bwaves_s.executable] + ['bwaves_1']
bwaves_s.input = 'bwaves_1.in'
#bwaves_s.output = out_dir + 'bwaves.out'

#503.cactuBSSN_r
cactuBSSN_r = Process()
cactuBSSN_r.executable = 'cactusBSSN_r' + x86_suffix
# REF CMDS
cactuBSSN_r.cmd = [cactuBSSN_r.executable] + ['spec_ref.par']
#cactuBSSN_r.output = out_dir + 'cactuBSSN.out'

#603.cactuBSSN_s
cactuBSSN_s = Process()
cactuBSSN_s.executable = 'cactuBSSN_s' + x86_suffix
# REF CMDS
cactuBSSN_s.cmd = [cactuBSSN_s.executable] + ['spec_ref.par']
#cactuBSSN_s.output = out_dir + 'cactuBSSN.out'

#503.namd_r
namd_r = Process()
namd_r.executable = 'namd_r' + x86_suffix
# REF CMDS
namd_r.cmd = [namd_r.executable] + ['--input', 'apoa1.input', '--output', 'apoa1.ref.output', '--iterations', '65']
#namd_r.output = out_dir + 'namd.out'

#503.parest_r
parest_r = Process()
parest_r.executable = 'parest_r' + x86_suffix
# REF CMDS
parest_r.cmd = [parest_r.executable] + ['ref.prm']
#parest_r.output = out_dir + 'parest.out'

#503.povray_r
povray_r = Process()
povray_r.executable = 'povray_r' + x86_suffix
# REF CMDS
povray_r.cmd = [povray_r.executable] + ['SPEC-benchmark-ref.ini']
#povray_r.output = out_dir + 'povray.out'

#503.lbm_r
lbm_r = Process()
lbm_r.executable = 'lbm_r' + x86_suffix
# REF CMDS
lbm_r.cmd = [lbm_r.executable] + ['3000', 'reference.dat', '0', '0', '100_100_130_ldc.of']
#lbm_r.output = out_dir + 'lbm.out'

#603.lbm_s
lbm_s = Process()
lbm_s.executable = 'lbm_s' + x86_suffix
# TEST, TRAIN, REF CMDS
lbm_s.cmd = [lbm_s.executable] + ['2000', 'reference.dat', '0', '0', '200_200_260_ldc.of']
#lbm_s.output = out_dir + 'lbm.out'

#503.wrf_r
wrf_r = Process()
wrf_r.executable = 'wrf_r' + x86_suffix
# TEST, TRAIN, REF CMDS
wrf_r.cmd = [wrf_r.executable]
#wrf_r.output = out_dir + 'wrf.out'

#603.wrf_s
wrf_s = Process()
wrf_s.executable = 'wrf_s' + x86_suffix
# TEST, TRAIN, REF CMDS
wrf_s.cmd = [wrf_s.executable]
#wrf_s.output = out_dir + 'wrf.out'

#503.blender_r
blender_r = Process()
blender_r.executable = 'blender_r' + x86_suffix
# TEST, TRAIN, REF CMDS
blender_r.cmd = [blender_r.executable] + ['sh3_no_char.blend', '-render-output', 'sh3_no_char_', \
					'--threads', '1', '-b', '-F', 'RAWTGA', '-s', '849', '-e', '849', '-a']
#blender_r.output = out_dir + 'blender.out'

#503.cam4_r
cam4_r = Process()
cam4_r.executable = 'cam4_r' + x86_suffix
# TEST, TRAIN, REF CMDS
cam4_r.cmd = [cam4_r.executable]
#cam4_r.output = out_dir + 'cam4.out'

#603.cam4_s
cam4_s = Process()
cam4_s.executable = 'cam4_s' + x86_suffix
# TEST, TRAIN, REF CMDS
cam4_s.cmd = [cam4_s.executable]
#cam4_s.output = out_dir + 'cam4.out'

#503.imagick_r
imagick_r = Process()
imagick_r.executable = 'imagick_r' + x86_suffix
# TEST, TRAIN, REF CMDS
imagick_r.cmd = [imagick_r.executable] + ['-limit disk', '0', 'refrate_input.tga', '-edge', \
					'41', '-resample', '181%', '-emboss', '31', \
					'-colorspace', 'YUV', '-mean-shift', '19x19+15%', '-resize', \
					'30%', 'refrate_output.tga']
#imagick_r.output = out_dir + 'imagick.out'

#603.imagick_s
imagick_s = Process()
imagick_s.executable = 'imagick_s' + x86_suffix
# TEST, TRAIN, REF CMDS
imagick_s.cmd = [imagick_s.executable] + ['-limit disk', '0', 'refspeed_input.tga', '-resize', \
					'817%', '-rotate', '-2.76', '-shave', '540x375', \
					'-alpha', 'remove', '-auto-level', '-contrast-stretch', \
					'1x1%', '-colorspace', 'Lab', '-channel', 'R', '-equalize', \
					'+channel', '-colorspace', 'sRGB', '-define', \
					'histogram:unique-colors=false', '-adaptive-blur', '0x5', \
					'-despeckle', '-auto-gamma', '-adaptive-sharpen', '55', \
					'-enhance', '-brightness-contrast', '10x10', '-resize', \
					'30%', 'refspeed_output.tga']
#imagick_s.output = out_dir + 'imagick.out'

#503.nab_r
nab_r = Process()
nab_r.executable = 'nab_r' + x86_suffix
# TEST, TRAIN, REF CMDS
nab_r.cmd = [nab_r.executable] + ['1am0', '1122214447', '122']
#nab_r.output = out_dir + 'nab.out'

#603.nab_s
nab_s = Process()
nab_s.executable = 'nab_s' + x86_suffix
# TEST, TRAIN, REF CMDS
nab_s.cmd = [nab_s.executable] + ['3j1n', '20140317', '220']
#nab_s.output = out_dir + 'nab.out'

#503.fotonik3d_r
fotonik3d_r = Process()
fotonik3d_r.executable = 'fotonik3d_r' + x86_suffix
# TEST, TRAIN, REF CMDS
fotonik3d_r.cmd = [fotonik3d_r.executable]
#fotonik3d_r.output = out_dir + 'fotonik3d.out'

#603.fotonik3d_s
fotonik3d_s = Process()
fotonik3d_s.executable = 'fotonik3d_s' + x86_suffix
# TEST, TRAIN, REF CMDS
fotonik3d_s.cmd = [fotonik3d_s.executable]
#fotonik3d_s.output = out_dir + 'fotonik3d.out'

#503.roms_r
roms_r = Process()
roms_r.executable = 'roms_r' + x86_suffix
# TEST, TRAIN, REF CMDS
roms_r.cmd = [roms_r.executable]
roms_r.input = 'ocean_benchmark2.in.x'
#roms_r.output = out_dir + 'roms.out'

#603.roms_s
roms_s = Process()
roms_s.executable = 'sroms' + x86_suffix
# TEST, TRAIN, REF CMDS
roms_s.cmd = [roms_s.executable]
roms_s.input = 'ocean_benchmark3.in.x'
#roms_s.output = out_dir + 'roms.out'


