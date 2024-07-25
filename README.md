<div align="center">

<table width=100%>
  <tr>
    <th width=10% align=center><strong>
    imgrot
      </strong>
    </th>
    <th width=90% align=right>
      <a href="https://hub.docker.com/r/robotwranglers/imgrot"><img src="https://img.shields.io/badge/dockerhub-imgrot-blue"><img src="https://img.shields.io/docker/v/robotwranglers/imgrot"></a>
    </th>
  </tr>
  <tr>
    <td width=10%><img src=https://raw.githubusercontent.com/Robot-Wranglers/docker-imgrot/master/img/icon.png style="width:150px"></td>
    <td width=90% align=center>
    <center>
    Tool for creating 3D rotation gifs from 2D images<br/>
    <img align=center width=150px src=img/demo.gif>
    </center>
    </td>
  </tr>
</table>
</div>

## Overview

A fork / update for the excellent original work at [eborboihuc/rotate_3d](https://github.com/eborboihuc/rotate_3d).

The original uses `opencv` to rotate 2d -> 3d.  This version adds better CLI parsing, support for python3, newer opencv, ability to animate and render animations with `ffmpeg`, and works via docker.

Different kinds of rotation are supported as well (see the end of this page for [a gallery](#changing-axis-of-rotation)).  Besides creating gifs, it can display them inside a terminal, using [chafa](https://github.com/hpjansson/chafa).

See also [the original docs](docs/README.original.md)

-------------------------------------

## Installation

Nothing on pypi.  See [dockerhub](https://hub.docker.com/r/robotwranglers/imgrot) for available releases.

```
pip install -r requirements.txt
```

-------------------------------------

## Usage

**Basic usage info follows:**

```bash
Usage: imgrot.py [OPTIONS] IMG_PATH

Options:
  --bg TEXT               Background color to pass to chafa
  --display               Display output with chafa
  --invert                Pass --invert to chafa
  --img-shape TEXT        Ideal image shape in WxH format (optional)
  --duration TEXT         Duration argument to pass to chafa
  --output-dir TEXT       Output directory for frames
  --output-file TEXT      Output file for animated gif
  --range TEXT            Range to rotate through
  --stream / --no-stream  Stream output in raw format (for use with pipes).
                          Implies --animate
  --verbose               Whether or not ffmpeg-stderr is displayed
  --view                  View a file with chafa (generates nothing)
  --rotation TEXT         One of { x | y | yz }
  --speed TEXT            Speed factor to pass to ffmpeg (default=.08)
  --stretch               Whether to pass --stretch to chafa
  --help                  Show this message and exit.

```

You can also set `LOGLEVEL=debug` for more info.

-------------------------------------

## Usage from Docker

A few examples of usage from docker:

#### Saving an Animation

```bash
$ docker run -it --rm -v `pwd`:/workspace -w /workspace robotwranglers/imgrot img/icon.png --range 360 --img-shape 200x200  --stream > demo.gif
```

<p align=center>
<img width=25% align=center src=img/demo.gif>
</p>

#### Terminal-Friendly Display 

```bash 
$ docker run -it --rm -v `pwd`:/workspace -w /workspace robotwranglers/imgrot img/icon.png --display --stretch --bg lightblue
```

<p align=center>
<img width=50% align=center src=img/demo.chafa.gif>
</p>

Note that this tries to respect transparency in the original image, but for more contrast with black images on black terminals, you can effectively add highlights by passing '--bg' arguments that go through to chafa.

------------------------------

#### Changing Axis of Rotation

The rotation can be controlled to create a bunch of different effects:

```bash 
$ docker run -it --rm -v `pwd`:/workspace \
  -w /workspace robotwranglers/imgrot \
  img/icon.png \
    --display --stretch \
    --bg darkgreen \
    --rotation <some-rotation here>
```

<p align=center>
<table>
  <tr>
    <th>x</th>
    <th>y</th>
    <th>s,swivel</th>
  </tr>  
  <tr>
    <td>
      <img src=img/rx.gif></td>
    <td>
      <img src=img/ry.gif>
      </td>
    <td><img src=img/rs.gif></td>
  </tr>
  <tr>
    <th>j,jitter</th>
    <th>w,wobble</th>
    <th>f,flip</th>
  </tr>  
  <tr>
    <td>
      <img src=img/rj.gif></td>
    <td>
      <img src=img/rw.gif>
      </td>
    <td><img src=img/rf.gif></td>
  </tr>
  <tr>
    <th>exit-ul</th>
    <th>exit-ur</th>
    <th>exit-lr</th>
  </tr>
  <tr>
    <td>
      <img src=img/rul.gif></td>
    <td>
      <img src=img/rur.gif>
      </td>
    <td><img src=img/rlr.gif></td>
  </tr>
  </table>
</p>
