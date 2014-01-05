#!/opt/local/bin/python
# encoding: utf-8
'''
blm (BlinkenLight Movie) file to Hacklace2 hex string converter

@author:     entropynil
@copyright:  2014 entropynil. All rights reserved.
@license:    GPLv3
@contact:    twitter:@entropynil | jabber:entropynil@jabber.ccc.de
'''

import sys, os, types, re
from argparse import ArgumentParser, RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2014-01-05'
__updated__ = '2014-01-05'

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def blm2hacklace2(filepath, verbose = False):

    if verbose: print 'blm2hacklace2 converts ' + filepath
    
    f = open(filepath,'r')
    
    # check file format and get width and height
    l = f.readline()
    if not l.lower().startswith("# blinkenlights movie"):
        raise Exception("Wrong BLM file format for file %s" % filepath)
    r = re.findall("(\d+)x(\d+)", l)
    if not (len(r)>0 and len(r[0])==2):
        raise Exception("Wrong BLM file format for file %s" % filepath)
    width = int(r[0][0])
    height = int(r[0][1])
    if height!=8:
        raise Exception("Only height of 8 is supported.")
    if width>200:
        raise Exception("Only width up to 200 is supported.")

    frameNo = 0
    for l in f:
        if l[0]=='@':
            frameNo += 1
            if verbose: print "%d. BLM frame %d x %d" % (frameNo, width, height)
            framestr = '1F %.2X' % width
            m = []
            for row in range(0, height):
                l = f.next()
                if len(l) > width:
                    l = l[:width]
                m.append(list(l))
                if verbose: print '      ' + '  '.join([s for s in list(l)])
            if verbose: print (8+3*(width-1))*'-'
            m = [list(i) for i in zip(*m)] # transpose
            for col in range(0, width):
                framestr += ' %.2X' % int(''.join(m[col])[::-1], 2)
            print framestr
    f.close()

def main(argv=None):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s 
  %s

  Copyright 2014 entropynil. All rights reserved.

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

USAGE
''' % (program_version_message, program_shortdesc)
    try:
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v","--verbose", help="verbose output", action="store_true")
        parser.add_argument(dest="filename", help="path to BLM file", metavar="filename")
        args = parser.parse_args()
        
        if not ('filename' in args and type(args.filename) == types.StringType and len(args.filename)>0):
            raise Exception("Filename missing, wrong type or zero length")
        if not os.path.isfile(args.filename):
            raise Exception("Invalid path to file %s" % args.filename)

        blm2hacklace2(args.filename, args.verbose)
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())