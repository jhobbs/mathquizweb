def svg_rectangle(width, height, solid=False):
    # find the longest and scale it to max size
    if width > height:
        scale = height / float(width)
        scaled_width = 150
        scaled_height = int(scale * scaled_width)
    else:
        scale = width / float(height)
        scaled_height = 150
        scaled_width = int(scale * scaled_height)

    y_label_x = scaled_width + 5
    y_label_y = max(15, scaled_height/2)

    x_label_x = int(scaled_width / 2)
    x_label_y = scaled_height + 20

    if solid:
        style = "fill:black;stroke:black;"
    else:
        style = "fill-opacity:0;stroke-width:1;stroke:black"

    text = (
    '<svg width="200" height="200">'
    '<rect width="%s" height="%s" style="%s"></rect>'
      '<text x="%s" y="%s">%s</text>'
      '<text x="%s" y="%s">%s</text>'
    '</svg>') % (
            scaled_width, scaled_height, style,
            y_label_x, y_label_y, height,
            x_label_x, x_label_y, width)
    return text


shape_to_svg_handlers = {
        'rectangle': svg_rectangle,
    }


def shape_to_svg(shape_type, shape_properties):
    handler = shape_to_svg_handlers[shape_type]
    result = handler(**shape_properties)
    return result


def get_shape_svgs(question):
    return [shape_to_svg(shape_type, shape_properties)
            for shape_type, shape_properties
            in question.graphic_cue.iteritems()]
