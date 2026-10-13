# VR Guide — RGB-D Reconstruction and Proximity Feedback

An undergraduate capstone project exploring how a reconstructed physical environment can support visual guidance in VR. The project combined RGB-D scene reconstruction, point-cloud meshing, and distance-based coloring to make nearby surfaces visible during interaction.

**Game Capstone Design · Kyung Hee University · September–December 2023 · Team project**

This repository preserves the project's point-cloud processing scripts and Unity assets. The complete capture pipeline and Unity application are not included in this snapshot.

## Project overview

The project investigated a context- and geometry-aware assistance system for interacting with real objects while wearing a VR headset. Development covered three stages:

1. **Reconstruct the environment:** use Azure Kinect RGB-D input with an ORB-SLAM2-based dense mapping pipeline.
2. **Prepare geometry for Unity:** convert point clouds to triangle meshes, then reduce geometric complexity for rendering.
3. **Visualize proximity:** color reconstructed surfaces according to their distance from the camera.

The broader proposal also considered semantic object retrieval and route guidance. Those components are not implemented in the code preserved here.

## Included components

| Component | Implementation |
| --- | --- |
| Point-cloud conversion | Open3D scripts for PLY/PCD conversion. |
| Surface reconstruction | Normal estimation and Ball Pivoting, followed by removal of degenerate triangles, duplicate geometry, and non-manifold edges. |
| Geometry assets | Point-cloud samples and exported OBJ/FBX files for inspection and use in Unity. |
| Proximity visualization | A Unity vertex/fragment shader that maps camera-to-vertex distance to color. |

The shader maps distance from red at the camera position toward white at **2 Unity world units**, then stays white beyond that threshold. Despite its `DistanceFadeShader` filename, the current implementation changes RGB color and outputs alpha = 1.

## Repository structure

```text
PointCloudToMesh/
├── PlyToPcd/
│   ├── PlyToPcd.py       # PLY ↔ PCD conversion
│   ├── map.ply
│   └── map.pcd
└── PcdToOBJ/
    ├── PcdToOBJ.py       # Point cloud → triangle mesh
    ├── map.pcd
    └── bpa_mesh.obj
Unity/
└── Object/
    ├── Bottle.fbx
    ├── Room.obj
    ├── p_mesh_c.obj
    └── Mat/
        ├── DistanceFadeShader.shader
        └── DisatanceFadeMaterial.mat
```

## Using the point-cloud scripts

The scripts use Python, NumPy, and Open3D. The original package versions were not recorded in the repository.

```bash
python -m venv .venv
# Activate the environment using the command for your operating system.
python -m pip install numpy open3d
```

Run each script from its own directory: input and output paths are relative to the working directory.

### Reconstruct a mesh

1. Open `PointCloudToMesh/PcdToOBJ/PcdToOBJ.py`.
2. Change `dataname` from `"voxel_pcd.pcd"` to `"map.pcd"` to use the included sample, or provide your own point-cloud filename. The default `voxel_pcd.pcd` is not included.
3. Run the script:

   ```bash
   cd PointCloudToMesh/PcdToOBJ
   python PcdToOBJ.py
   ```

The script writes `bpa_mesh.obj`, replacing the existing file with that name. Change the output filename first if you want to keep the supplied mesh.

The active reconstruction method is Ball Pivoting. The file also retains a commented-out Poisson reconstruction example; downsampling and decimation lines are disabled in the current script.

### Convert point-cloud formats

`PlyToPcd.py` contains two independent conversions:

- `map.ply` → `map.pcd`
- `voxel_pcd.pcd` → `voxel_pcd.ply`

The second input is not included. Comment out that block or provide the file before running the script from `PointCloudToMesh/PlyToPcd/`.

## Inspecting the Unity assets

`Unity/` is an asset collection, not a Unity Hub project: it does not contain `Assets/`, `Packages/`, or `ProjectSettings/`.

To inspect the visualization, import the contents of `Unity/Object/` into an existing Unity project's `Assets/` folder. Create a material using `Custom/DistanceFadeShader`, apply it to a mesh, and move the camera relative to the geometry. The shader uses `UnityCG.cginc` and Built-in Render Pipeline conventions; compatibility with URP/HDRP has not been established.

The original course prototype used Oculus Quest 2. This snapshot does not include the XR rig, scenes, or headset configuration needed to reproduce that application.

## Team and provenance

Developed by **Inhyuk Song (송인혁)** and **전재현** for Game Capstone Design at Kyung Hee University.

This is a snapshot of the original team repository, re-hosted by a project member:
[23-2-GameCapstoneDseign/VR_Guide_Program](https://github.com/23-2-GameCapstoneDseign/VR_Guide_Program).

The original reconstruction work built on
[ORB-SLAM2 with point-cloud mapping](https://github.com/gaoxiang12/ORBSLAM2_with_pointcloud_map).
Point-cloud processing uses [Open3D](https://www.open3d.org/).
