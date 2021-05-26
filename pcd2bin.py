# Module:       pcd2bin.py
# Description:  .pcd to .bin converter
#
# Author:       DinghaoYang (dinghowyang@gmail.com) and Yuseung Na (ys.na0220@gmail.com)
# Version:      1.1
#
# Revision History
#       January 19, 2021: Yuseung Na, Created
#       May 25, 2021: Dinghao Yang, Modified

import numpy as np
import os
import argparse
import pcl
import csv
from tqdm import tqdm

def main():
    ## Add parser
    parser = argparse.ArgumentParser(description="Convert .pcd to .bin")
    parser.add_argument(
        "--pcd_path",
        help=".pcd file path.",
        type=str,
        default="/home/user/lidar_pcd"
    )
    parser.add_argument(
        "--bin_path",
        help=".bin file path.",
        type=str,
        default="/home/user/lidar_bin"
    )
    args = parser.parse_args()

    ## Find all pcd files
    pcd_files = []
    for (path, dir, files) in os.walk(args.pcd_path):
        for filename in files:
            # print(filename)
            ext = os.path.splitext(filename)[-1]
            if ext == '.pcd':
                pcd_files.append(path + "/" + filename)

    ## Sort pcd files by file name
    pcd_files.sort()   
    print("Finish to load point clouds!")

    ## Make bin_path directory
    try:
        if not (os.path.isdir(args.bin_path)):
            os.makedirs(os.path.join(args.bin_path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print ("Failed to create directory!")
            raise

    ## Generate csv meta file
    csv_file_path = os.path.join(args.bin_path, "meta.csv")
    csv_file = open(csv_file_path, "w")
    meta_file = csv.writer(
        csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    ## Write csv meta file header
    meta_file.writerow(
        [
            "pcd file name",
            "bin file name",
        ]
    )
    print("Finish to generate csv meta file")

    ## Converting Process
    print("Converting Start!")
    seq = 0
    for pcd_file in tqdm(pcd_files):
        ## Get pcd file
        # pc = pypcd.PointCloud.from_path(pcd_file)
        pc = pcl.load_XYZI(pcd_file)
        pc = np.array(pc.to_array(), dtype=np.float32)

        ## Generate bin file name
        bin_file_name = pcd_file.split('/')[-1].split('.')[0] + '.bin'
        print(bin_file_name)
        bin_file_path = os.path.join(args.bin_path, bin_file_name)
        
        ## Get data from pcd (x, y, z, intensity)
        np_x = (np.array(pc[:, 0], dtype=np.float32)).astype(np.float32)
        np_y = (np.array(pc[:, 1], dtype=np.float32)).astype(np.float32)
        np_z = (np.array(pc[:, 2], dtype=np.float32)).astype(np.float32)
        np_i = (np.array(pc[:, 3], dtype=np.float32)).astype(np.float32)/256

        ## Stack all data    
        points_32 = np.transpose(np.vstack((np_x, np_y, np_z, np_i)))

        ## Save bin file                                    
        points_32.tofile(bin_file_path)

        ## Write csv meta file
        meta_file.writerow(
            [os.path.split(pcd_file)[-1], bin_file_name]
        )

        seq = seq + 1
    
if __name__ == "__main__":
    main()