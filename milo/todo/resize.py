#!/usr/bin/env python

import os
import glob

from PIL import Image
import PIL.ExifTags

#template for index.html
main_template = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2//EN">

<html>
<head>
  <style type="text/css">img{{ margin: 20px;}}</style>
  <title>Some Photos</title>
</head>

<body>

    <h2>Click any photo to see a larger image.</h2>

{0}

</body>
</html>
"""

#template for an individual photo page
sub_template = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2//EN">

<html>
<head>
  <style type="text/css">img{{ margin: 20px;}}</style>
  <title>{filename}</title>
</head>

<body>
    <h2>Click photo or "next" for previous image.</h2>
    <a href='index.html#{filename}'>back</a><br/>
    <a href='{prev_img}.html'>previous</a> <a href='{next_img}.html'>next<br/>
    <img src="{filename}" alt="image" /></a>
    <br/>
    {filename}<br/>

</body>
</html>
"""

img_template = (
    '<a name="{small}" href="{small}.html">' +
    '<img src="{thumb}" alt="image" /></a>'
)

def resize_file(filename, max_size=1024, label='small', location='.'):

    image = Image.open(filename)

    #determine whether image is
    #portrait or landscape
    try:
        info = image._getexif()
        for tag, value in info.items():
            decoded = PIL.ExifTags.TAGS.get(tag, tag)
            if decoded == 'Orientation':
                if value in (0, 1):
                    pass
                elif value in (3, 8):
                    #rotate before resizing
                    #calculation
                    image = image.rotate(90)
                elif value == 6:
                    #rotate before resizing
                    #calculation
                    image = image.rotate(270)
                else:
                    raise ValueError('unexpected orientation {0}, {1}'.format(value, filename))

        tag_items = info.items()
    except AttributeError:
        pass

    if not os.path.exists(location):
        os.mkdir(location)

    width, height = [float(x) for x in image.size]

    file_parts = filename.split(os.extsep)
    file_parts.insert(-1, '_{0}'.format(label))
    new_name = ''.join(file_parts[:-1]) + os.extsep + file_parts[-1]
    new_path = os.path.join(location, new_name)

    if width <= max_size and height <= max_size:
        image.save(new_path)

    else:

        if width >= height:
            ratio = height / width
            new_size = (max_size, int(max_size * ratio))
        else:
            ratio = width / height
            new_size = (int(max_size * ratio), max_size)

        if not os.path.exists(new_path):
            smaller = image.resize(new_size)
            smaller.save(new_path)

    return new_name

if __name__ == '__main__':

    extensions = ('jpg', 'gif', 'png')

    extensions = extensions + tuple([x.upper() for x in extensions])

    location = './images_html'

    tags = []

    files = []

    for ext in extensions:

        for filename in glob.glob('*.{0}'.format(ext)):

            small = resize_file(filename, location=location)
            thumb = resize_file(filename, max_size=300, label='thumb', location=location)
    
            if small is None or thumb is None:
                continue
            
            files.append((small, thumb))


    for index, (small, thumb) in enumerate(sorted(files)):

            tags.append(
                img_template.format(small=small, thumb=thumb)
            ) 

            prev_img, next_img = None, None

            try:
                prev_img = files[index-1][0]
            except IndexError:
                prev_img = files[-1][0]

            try:
                next_img = files[index+1][0]
            except IndexError:
                next_img = files[0][0]

            html = sub_template.format(filename=small, prev_img=prev_img, next_img=next_img)
            with open(os.path.join(location, small + '.html'), 'w') as output:
                output.write(html)

    html = main_template.format('\n'.join(tags))
    with open(os.path.join(location, 'index.html'), 'w') as output:
        output.write(html)



