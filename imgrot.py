"""
# Usage:
#  Change main function with ideal arguments
#  then
#  python imgrot.py [name of the image] [degree to rotate] ([ideal width] [ideal height])
#  e.g.,
#  python imgrot.py img/000001.jpg 360
#  python imgrot.py img/000001.jpg 45 500 700
#
# Parameters:
#  img_path  : path of image that you want rotated
#  shape     : ideal shape of input image, None for original size.
#  theta     : rotation around the x axis
#  phi       : rotation around the y axis
#  gamma     : rotation around the z axis (basically a 2D rotation)
#  dx        : translation along the x axis
#  dy        : translation along the y axis
#  dz        : translation along the z axis (distance to the image)
"""

import os
import sys
import logging
import subprocess

import click

from image_transformer import ImageTransformer

# Setup logging
log_level = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - imgrot - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


# Setup CLI interface
@click.command()
@click.option("--bg", default="black", help="Background color to pass to chafa")
@click.option(
    "--display", is_flag=True, default=False, help="Display output with chafa"
)
@click.option("--invert", is_flag=True, default=False, help="Pass --invert to chafa")
@click.option(
    "--img-shape", default=None, help="Ideal image shape in WxH format (optional)"
)
@click.option(
    "--duration",
    default="",
    help="Duration argument to pass to chafa",
)
@click.option("--output-dir", default="/tmp/imgrot", help="Output directory for frames")
@click.option(
    "--output-file", default="/tmp/imgrot.gif", help="Output file for animated gif"
)
@click.option("--range", "rot_range", default="360", help="Range to rotate through")
@click.option(
    "--stream/--no-stream",
    default=False,
    help="Stream output in raw format (for use with pipes).  Implies --animate",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Whether or not ffmpeg-stderr is displayed",
)
@click.option(
    "--view",
    is_flag=True,
    default=False,
    help="View a file with chafa (generates nothing)",
)
@click.option("--rotation", default="y", help="One of { x | y | yz }")
@click.option(
    "--speed", default=".08", help="Speed factor to pass to ffmpeg (default=.08)"
)
@click.option(
    "--stretch",
    is_flag=True,
    default=False,
    help="Whether to pass --stretch to chafa",
)
@click.argument("img_path", required=True)
def run(
    img_path: str,
    stretch: bool = False,
    duration: str = "",
    display: bool = False,
    invert: bool = False,
    verbose: bool = False,
    img_shape=None,
    speed: str = "0.08",
    rotation: str = "y",
    bg: str = "black",
    output_dir: str = "/tmp",
    output_file: str = "/tmp/imgrot.gif",
    rot_range: str = "360",
    stream: bool = False,
    view: bool = False,
):
    stretch = "--stretch" if stretch else ""
    duration = f"--duration {duration}" if duration else ""
    invert = invert and "--invert" or ""
    bg = f"--bg {bg}"

    if not os.path.exists(img_path):
        logger.debug(f"{img_path} does not exist!")
        raise SystemExit(1)

    rot_range = int(rot_range)
    img_shape = img_shape and list(map(int, img_shape.split("x")))
    it = ImageTransformer(img_path, img_shape)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    logger.debug(f"Rotating {img_path} .. ")
    for ang in range(0, rot_range):
        rotated_img = it.rotate_along_axis(**it.get_rotation_args(rotation, ang))
        fname = f"{output_dir}/{str(ang).zfill(3)}.png"
        it.save_image(fname, rotated_img)
    logger.debug("Done")

    command = f"ls {output_dir}/|wc -l"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logger.debug(f"Command failed with return code {result.returncode}\n")
        raise SystemExit(result.returncode)
    else:
        logger.debug(f"Total Frames: {result.stdout.strip()}")
    logger.debug("Animating..")
    quiet_maybe = "" if verbose else "2> /dev/null"
    commands = [
        f"ffmpeg -y -i {output_dir}/000.png -vf palettegen=reserve_transparent=1 /tmp/palette.png {quiet_maybe}",
        f"ffmpeg -y -framerate 140 -pattern_type glob -i '{output_dir}/*.png' -i /tmp/palette.png -lavfi paletteuse=alpha_threshold=128 -gifflags -offsetting /tmp/.tmp.gif {quiet_maybe}",
        f"""ffmpeg -y -i /tmp/.tmp.gif  -vf "split[s0][s1];[s0]palettegen[p];[s1]setpts={speed}*PTS[v];[v][p]paletteuse" {output_file} {quiet_maybe}""",
    ]
    for cmd in commands:
        logger.debug(cmd)
        result = subprocess.run(cmd, shell=True, stdout=sys.stderr, stderr=sys.stderr)
        if result.returncode != 0:
            logger.critical(f"Command failed with return code {result.returncode}")
            raise SystemExit(result.returncode)
    if view:
        logger.debug(f"Viewing {img_path}")
        os.system(f"chafa {stretch} {duration} {img_path}")
    elif display:
        logger.debug("Displaying animated gif..")
        os.system(
            f"chafa {bg} {duration} {stretch} {invert} --symbols 'braille' {output_file}"
        )
    elif stream:
        logger.debug("Streaming animation..")
        os.system(
            f"convert {output_file} -fuzz 10% -transparent white {output_file} {quiet_maybe}"
        )
        with open(output_file, "rb") as binary_file:
            content = binary_file.read()
            sys.stdout.buffer.write(content)
    else:
        logger.critical("No instructions, not sure what to do")
        raise SystemExit(1)


if __name__ == "__main__":
    run()
