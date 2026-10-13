import open3d as o3d
pcd = o3d.io.read_point_cloud("map.ply")

o3d.io.write_point_cloud("map.pcd" , pcd)


ply = o3d.io.read_point_cloud("voxel_pcd.pcd")

o3d.io.write_point_cloud("voxel_pcd.ply" , ply)

