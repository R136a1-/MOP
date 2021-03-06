#!/usr/bin/env python
################################################################################
##                                                                            ##
## Copyright 2013 by its authors                                              ##
## See COPYING, AUTHORS                                                       ##
##                                                                            ##
## This file is part of OSSOS Moving Object Pipeline (OSSOS-MOP)              ##
##                                                                            ##
##    OSSOS-MOP is free software: you can redistribute it and/or modify       ##
##    it under the terms of the GNU General Public License as published by    ##
##    the Free Software Foundation, either version 3 of the License, or       ##
##    (at your option) any later version.                                     ##
##                                                                            ##
##    OSSOS-MOP is distributed in the hope that it will be useful,            ##
##    but WITHOUT ANY WARRANTY; without even the implied warranty of          ##
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           ##
##    GNU General Public License for more details.                            ##
##                                                                            ##
##    You should have received a copy of the GNU General Public License       ##
##    along with OSSOS-MOP.  If not, see <http://www.gnu.org/licenses/>.      ##
##                                                                            ##
################################################################################
'''run step2 of the OSSOS pipeline.'''

import os
import argparse
import logging
from ossos import util
from ossos import storage

def step2(expnums, ccd, version, prefix=None):
    '''run the actual step2  on the given exp/ccd combo'''

    jmp_args = ['step2jmp']
    matt_args = ['step2matt_jmp']

    idx = 0
    for expnum in expnums:
        jmp_args.append(
            storage.get_image(expnum,
                              ccd=ccd,
                              version=version,
                              ext='obj.jmp',
                              prefix=prefix
                              )[0:-8]
            )
        idx += 1
        matt_args.append('-f%d' % ( idx))
        matt_args.append(
            storage.get_image(expnum,
                              ccd=ccd,
                              version=version,
                              ext='obj.matt',
                              prefix=prefix
                              )[0:-9]
            )

    util.exec_prog(jmp_args)
    util.exec_prog(matt_args)

    for expnum in expnums:
        for ext in ['unid.jmp', 'unid.matt', 'trans.jmp']:
            uri = storage.dbimages_uri(expnum,ccd=ccd,version=version,ext=ext, prefix=prefix)
            filename = os.path.basename(uri)
            storage.copy(filename, uri)


    return

if __name__ == '__main__':
    ### Must be running as a script

    parser=argparse.ArgumentParser(
        description='Run step2jmp and step2matt on a given exposure.')

    parser.add_argument("--ccd","-c",
                        action="store",
                        default=None,
                        type=int,
                        dest="ccd")
    parser.add_argument("--fk", action="store_true", default=False, help="Do fakes?")
    parser.add_argument("--dbimages",
                        action="store",
                        default="vos:OSSOS/dbimages",
                        help='vospace dbimages containerNode')
    parser.add_argument("expnums",
                        type=int,
                        nargs=3,
                        help="3 expnums to process")
    parser.add_argument("--version",
                        action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-t','--type',
                        help='which type of image to process',
                        choices=['s','p','o'],
                        default='p'
                        )
    parser.add_argument('--no-sort',
                        help='preserve input exposure order',
                        action='store_true')
    parser.add_argument("--verbose","-v",
                        action="store_true")
    parser.add_argument("--force", action="store_true")


    args=parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    storage.DBIMAGES = args.dbimages

    if args.ccd is None:
        ccdlist = range(0,36)
    else:
        ccdlist = [args.ccd]

    prefix = ( args.fk and "fk") or ""

    if not args.no_sort:
        args.expnums.sort()

    for ccd in ccdlist:
        try:
            message = storage.SUCCESS
            for expnum in args.expnums:
                if not storage.get_status(expnum, ccd, prefix+'step1', version=args.type):
                    raise IOError(35, "missing step1 for %s" % ( expnum))
            if storage.get_status(args.expnums[0],
                                  ccd,
                                  prefix+'step2',
                                  version=args.type) and not args.force:
                logging.info("Already did %s %s, skipping" %(str(expnum),
                                                             str(ccd)))
                continue
            logging.info("step2 on expnums :%s, ccd: %d" % (
                    str(args.expnums), ccd))
            step2(args.expnums, ccd, version=args.type, prefix=prefix)

        except Exception as e:
            message = str(e)
        logging.error(message)
        storage.set_status(args.expnums[0],
                           ccd,
                           prefix+'step2',
                           version=args.type,
                           status=message)
        
            
