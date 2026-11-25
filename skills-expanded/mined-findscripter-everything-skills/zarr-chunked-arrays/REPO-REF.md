# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 03-data/zarr-chunked-arrays/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当需要为超大 N 维科学数组（气候/遥感/影像）做分块、压缩与并行读写，或要把数据放到 S3/GCS 做云原生工作流，或与 NumPy/Dask/Xarray 互通时使用；做 Zarr 3 数组/组的创建、分块与分片策略选型、压缩编解码配置、云端 fsspec 存储与元数据合并，产出 .zarr 存储与读写代码；不适用于纯内存中小型数组（直接用 NumPy）或关系/表格数据（用 Parquet/数
