import numpy as np
import open3d as o3d

dataname="voxel_pcd.pcd"

pcd = o3d.io.read_point_cloud(dataname)

#pcd = pcd.voxel_down_sample(voxel_size=0.005)
print(1)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
print(2)
#o3d.visualization.draw_geometries([pcd])

# BPA(Ball-Pivoting Algorithm) Method
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)

radius = 5 * avg_dist
print(3)

bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))

print(4)

#dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)
dec_mesh = bpa_mesh
print(5)
dec_mesh.remove_degenerate_triangles()
dec_mesh.remove_duplicated_triangles()
dec_mesh.remove_duplicated_vertices()
dec_mesh.remove_non_manifold_edges()
print(6)
# Mesh Refinement
#dec_mesh.filter_smooth_laplacian(number_of_iterations=100, lambda_filter=10.5)

print(7)
o3d.io.write_triangle_mesh("bpa_mesh.obj", dec_mesh)


"""
#o3d.visualization.draw_geometries([dec_mesh])

# Poisson Method
poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=15, width=0, scale=1.1, linear_fit=False)[0]

bbox = pcd.get_axis_aligned_bounding_box()
p_mesh_crop = poisson_mesh.crop(bbox)

o3d.io.write_triangle_mesh("p_mesh_c.obj", p_mesh_crop)

#o3d.visualization.draw_geometries([p_mesh_crop])

"""