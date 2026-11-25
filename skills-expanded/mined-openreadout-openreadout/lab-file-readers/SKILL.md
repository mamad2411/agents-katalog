---
name: lab-file-readers
description: "Read raw lab-instrument files with the open-source Python readers and Bio-Formats command-line tools installed in this environment (also FT-IR/Raman spectra, qPCR, OpenLab CDS, screening plates, chromatographic peak integration). Covers light and electron microscopy (Zeiss CZI/ZVI/LSM, Nikon ND2, Leica LIF, Olympus OIR/OIF/VSI, OME-TIFF and TIFF variants, Imaris, MRC, Gatan DM3/DM4, FEI SER/EMD), flow cytometry (FCS), electrophysiology (Axon ABF, Neuralynx, Blackrock, SpikeGLX, Intan, Plexon, NWB), NMR (Bruker, Varian/Agilent, JEOL, JCAMP-DX), mass spectrometry (mzML, mzXML, imzML; Agilent .D and Waters .raw via rainbow), chromatography (Agilent ChemStation .D, Waters .raw, ANDI netCDF) and plate-reader exports. Use when a user has an instrument file and wants to know what is inside it, whether it is intact, a statistic of its data, or a conversion to an open format (OME-TIFF, CSV)."
---

# Reading lab-instrument files in this environment

`python3` on PATH has the readers below preinstalled (plus numpy, scipy, pandas, pyarrow, lxml,
h5py, zarr). Bio-Formats' command-line tools are on PATH too (Java is installed): `showinf`,
`bfconvert`, `formatlist`, `tiffcomment`, `xmlvalid`. The Python environment is read-only; to add
a package, make a venv that still sees the preinstalled readers:
`python3 -m venv --system-site-packages .venv && .venv/bin/pip install PACKAGE`.

## Pick a reader

| data | first choice | also |
| --- | --- | --- |
| any microscopy format | `bioio.BioImage(path)` | `showinf -nopix -omexml FILE` (Bio-Formats, ~160 formats) |
| Zeiss CZI | `czifile.CziFile` | `bioio` (bioio-czi) |
| Nikon ND2 | `nd2.ND2File` | `bioio` (bioio-nd2) |
| Leica LIF | `liffile.LifFile` | `readlif`, `bioio` (bioio-lif) |
| Olympus OIR / OIF | `oirfile.OirFile` / `oiffile.OifFile` | Bio-Formats |
| Olympus VSI, Zeiss ZVI, Imaris IMS, others | `showinf` / `bfconvert` | `h5py` for IMS |
| OME-TIFF, ImageJ TIFF, SVS, NDPI, LSM, STK | `tifffile.TiffFile` | `bioio` |
| Hamamatsu DCIMG | `dcimg.DCIMGFile` | |
| MRC / CCP4 | `mrcfile.open(path, permissive=True)` | |
| Gatan DM3/DM4, FEI SER/EMD | `ncempy.io.read(path)` | `dm4`, `h5py` (EMD) |
| FCS | `flowio.FlowData(path)` | `fcsparser.parse`, `flowkit.Sample` (gating, compensation) |
| Axon ABF | `pyabf.ABF(path)` | `neo.io.AxonIO` |
| Neuralynx, Blackrock, SpikeGLX, Intan, Plexon | `neo.io.get_io(path)` or the named `neo.io.*IO` | `neo.rawio` |
| NWB | `pynwb.NWBHDF5IO(path, "r").read()` | `h5py` |
| Bruker TopSpin directory | `nmrglue.bruker.read(dir)` / `read_pdata(dir + "/pdata/1")` | |
| Varian/Agilent VnmrJ, JEOL Delta | `nmrglue.varian.read`, `nmrglue.jeol.read` | |
| JCAMP-DX (`.jdx`, `.dx`) | `nmrglue.jcampdx.read` | `jcamp.readfile` |
| mzML / mzXML / imzML | `pyteomics.mzml.read`, `pyteomics.mzxml.read` | `pyimzml.ImzMLParser` |
| Agilent `.D` (ChemStation, MassHunter), Waters `.raw` | `rainbow.read(dir)` | |
| ANDI chromatography `.cdf` | `scipy.io.netcdf_file(path, "r", mmap=False)` | |
| plate-reader text/CSV/XLSX exports | `pandas` | |
| Agilent OpenLab CDS `.dx` | a zip: `zipfile`, then `rainbow.read(dir)` on the folder holding its `.CH` signal members | |
| chromatographic peaks (area, RT, height) | `pyopenms` (`PeakPickerChromatogram`, `PeakIntegrator`) | `scipy.signal.find_peaks`, `peak_widths` |
| high-content screening plates (Harmony `Index.idx.xml`/`Index.xml`, ImageXpress `.HTD`, CellVoyager `.mlf`) | `showinf -nopix` on the index file; `xml.etree` for the index; `tifffile` for the planes | `bioio` |
| Bruker OPUS (`.0`, `.1`, …) | `brukeropus.read_opus(path)` | `spectrochempy.read_opus` |
| Thermo OMNIC `.spa`/`.spg`, JCAMP-DX IR | `spectrochempy.read_omnic(path)`, `read_jcamp` | |
| Renishaw WiRE `.wdf` (Raman, maps) | `renishawWiRE.WDFReader(path)` | `spectrochempy.read_wdf` |
| qPCR RDML (`.rdml`) | `rdmlpython.Rdml(path)` | |
| Applied Biosystems `.eds` (QuantStudio, ViiA 7, 7500) | a zip: `zipfile` (XML/JSON/text results and amplification data inside) | vendor `.xls` exports: `xlrd` |
| unknown file | `file`, `xxd FILE \| head`, `showinf -nopix FILE` | |

No reader for Thermo `.raw`, Sciex `.wiff`, Bruker timsTOF `.d`, Bio-Rad `.pcrd` or PerkinElmer `.sp` is
available here (the vendors' readers need Windows or .NET; specio does not import on Python 3.12).

## Common calls

```python
from bioio import BioImage
img = BioImage("f.czi")                   # picks the plugin by extension
img.scenes, img.set_scene(0)              # series / positions / scenes
img.dims, img.shape                       # dims order is TCZYX
img.physical_pixel_sizes                  # (Z, Y, X) in µm
img.channel_names
img.get_image_data("ZYX", C=0, T=0)       # numpy array
img.metadata                              # the reader's native metadata (often XML)

import nd2
with nd2.ND2File("f.nd2") as f:
    f.sizes, f.voxel_size(), f.metadata, f.text_info, f.experiment, f.asarray()

import czifile
with czifile.CziFile("f.czi") as f:
    f.metadata(), f.scenes, f.asarray()   # metadata() is the embedded XML

import liffile
with liffile.LifFile("f.lif") as lif:
    for im in lif.images: im.name, im.sizes, im.coords, im.asarray()
    lif.xml_header

import tifffile
with tifffile.TiffFile("f.ome.tiff") as t:
    t.series, t.ome_metadata, t.imagej_metadata, t.pages[0].tags
tifffile.imwrite("out.ome.tiff", data, ome=True, photometric="minisblack",
                 metadata={"axes": "ZCYX", "PhysicalSizeX": 0.1, "PhysicalSizeY": 0.1,
                           "PhysicalSizeZ": 0.5})

import flowio
fd = flowio.FlowData("f.fcs")             # fd.text (keywords), fd.event_count, fd.channel_count
events = fd.as_array()                    # events x parameters; names in fd.pnn_labels / fd.pns_labels

import pyabf
abf = pyabf.ABF("f.abf")                  # abf.sweepCount, abf.dataRate, abf.abfDateTime
abf.setSweep(0, channel=0); abf.sweepX, abf.sweepY, abf.sweepUnitsY

import nmrglue as ng
dic, data = ng.bruker.read_pdata("exp/1/pdata/1")
udic = ng.bruker.guess_udic(dic, data); ppm = ng.fileiobase.uc_from_udic(udic).ppm_scale()

from pyteomics import mzml
with mzml.read("f.mzML") as r:
    for spec in r: spec["ms level"], spec["m/z array"], spec["intensity array"]

import rainbow
d = rainbow.read("run.D")                 # d.datafiles, d.get_file(name).xlabels/.ylabels/.data, d.metadata
```

```bash
showinf -nopix -omexml file.lif           # all metadata as OME-XML, no pixel reading
showinf -nopix -series 2 file.lif         # one series
bfconvert file.czi out.ome.tiff           # convert (keeps calibration); -series N, -channel N
```

## Looking at the data

matplotlib and Pillow are installed. To look at an image plane, a slide's low-resolution pyramid
level, a trace, a spectrum or a plate, save it as a PNG in the working directory and open it with
the Read tool, which shows you the picture; zoom by cropping a region at a finer level.

```python
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.imshow(plane, cmap="gray"); plt.colorbar(); plt.savefig("look.png", dpi=100)   # then Read look.png
from PIL import Image; Image.fromarray(rgb_uint8).save("slide.png")
```

## Checking integrity

Open the file with its reader and read every plane or record (or `showinf file` without
`-nopix`, which reads pixels); compare the expected size from the header with the file size.
Truncated files usually raise when the last planes or events are read.
