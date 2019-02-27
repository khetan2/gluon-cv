"""Pruned ResNetV1bs, implemented in Gluon."""
from __future__ import division
from mxnet.context import cpu
from mxnet.gluon import nn
from mxnet import ndarray
from .resnetv1b import *

__all__ = ['resnet18_v1b_2_point_6x', 'resnet50_v1d_1_point_8x', 'resnet50_v1d_3_point_6x', 'resnet50_v1d_5_point_9x',
           'resnet50_v1d_8_point_8x', 'resnet101_v1d_1_point_9x', 'resnet101_v1d_2_point_2x'
           ]


def prune_gluon_block(net, prefix, params, pretrained=False, ctx=cpu(0)):
    """
    :param prefix: prefix of the original resnet50_v1d
    :param pretrained: Boolean specifying if the pretrained model parameters needs to be loaded
    :param net: original network that is required to be pruned
    :param params: dictionary of parameters for the pruned network. Size of the parameters in this dictionary tells what
    should be the size of channels of each convolution layer.
    :param ctx: cpu(0)
    :return: "net"
    """
    for key, layer in net._children.items():
        if pretrained:
            if isinstance(layer, nn.BatchNorm):
                params_layer = layer._collect_params_with_prefix()
                for param_name in ['beta', 'gamma', 'running_mean', 'running_var']:
                    param_val = params[layer.name.replace(prefix, "resnetv1d") + "_" + param_name]
                    layer.params.get(param_name)._shape = param_val.shape
                    params_layer[param_name]._load_init(param_val, ctx=ctx)

        if isinstance(layer, nn.Conv2D):
            param_val = params[layer.name.replace(prefix, "resnetv1d") + "_weight"]
            layer._channels = param_val.shape[0]
            layer._kwargs['num_filter'] = param_val.shape[0]

            params_layer = layer._collect_params_with_prefix()
            for param_name in ['weight']:
                param_val = params[layer.name.replace(prefix, "resnetv1d") + "_" + param_name]
                layer.params.get(param_name)._shape = param_val.shape
                if pretrained:
                    params_layer[param_name]._load_init(param_val, ctx=ctx)

        if isinstance(layer, nn.Dense):
            layer._in_units = params[layer.name.replace(prefix, "resnetv1d") + "_weight"].shape[1]

            params_layer = layer._collect_params_with_prefix()
            for param_name in ['weight', 'bias']:
                param_val = params[layer.name.replace(prefix, "resnetv1d") + "_" + param_name]
                layer.params.get(param_name)._shape = param_val.shape
                if pretrained:
                    params_layer[param_name]._load_init(param_val, ctx=ctx)
        else:
            prune_gluon_block(layer, prefix, params, pretrained, ctx)


def resnet18_v1b_2_point_6x(pretrained=False, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
    """Constructs a ResNetV1b-18_2.6x model. Uses resnet18_v1b construction from resnetv1b.py

    Parameters
    ----------
    pretrained : bool or str
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    """
    model = ResNetV1b(BasicBlockV1b, [2, 2, 2, 2], name_prefix='resnetv1b_', **kwargs)

    from .model_store import get_model_file
    params_file = get_model_file('resnet%d_v%db_%.1fx' % (18, 1, 2.6), tag=pretrained, root=root)
    prune_gluon_block(model, model.name, ndarray.load(params_file), pretrained=pretrained, ctx=ctx)

    if pretrained:
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        model.synset = attrib.synset
        model.classes = attrib.classes
        model.classes_long = attrib.classes_long
    return model


def resnet50_v1d_1_point_8x(pretrained=False, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
    """Constructs a ResNetV1d-50_1.8x model. Uses resnet50_v1d construction from resnetv1b.py

    Parameters
    ----------
    pretrained : bool or str
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    """
    model = ResNetV1b(BottleneckV1b, [3, 4, 6, 3], deep_stem=True, avg_down=True,
                      name_prefix='resnetv1d_', **kwargs)

    from .model_store import get_model_file
    params_file = get_model_file('resnet%d_v%dd_%.1fx' % (50, 1, 1.8), tag=pretrained, root=root)
    prune_gluon_block(model, model.name, ndarray.load(params_file), pretrained=pretrained, ctx=ctx)

    if pretrained:
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        model.synset = attrib.synset
        model.classes = attrib.classes
        model.classes_long = attrib.classes_long
    return model


def resnet50_v1d_3_point_6x(pretrained=False, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
    """Constructs a ResNetV1d-50_3.6x model. Uses resnet50_v1d construction from resnetv1b.py

    Parameters
    ----------
    pretrained : bool or str
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    """
    model = ResNetV1b(BottleneckV1b, [3, 4, 6, 3], deep_stem=True, avg_down=True,
                      name_prefix='resnetv1d_', **kwargs)

    from .model_store import get_model_file
    params_file = get_model_file('resnet%d_v%dd_%.1fx' % (50, 1, 3.6), tag=pretrained, root=root)
    prune_gluon_block(model, model.name, ndarray.load(params_file), pretrained=pretrained, ctx=ctx)

    if pretrained:
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        model.synset = attrib.synset
        model.classes = attrib.classes
        model.classes_long = attrib.classes_long
    return model


def resnet50_v1d_5_point_9x(pretrained=False, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
    """Constructs a ResNetV1d-50_5.9x model. Uses resnet50_v1d construction from resnetv1b.py

    Parameters
    ----------
    pretrained : bool or str
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    """
    model = ResNetV1b(BottleneckV1b, [3, 4, 6, 3], deep_stem=True, avg_down=True,
                      name_prefix='resnetv1d_', **kwargs)

    from .model_store import get_model_file
    params_file = get_model_file('resnet%d_v%dd_%.1fx' % (50, 1, 5.9), tag=pretrained, root=root)
    prune_gluon_block(model, model.name, ndarray.load(params_file), pretrained=pretrained, ctx=ctx)

    if pretrained:
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        model.synset = attrib.synset
        model.classes = attrib.classes
        model.classes_long = attrib.classes_long
    return model


def resnet50_v1d_8_point_8x(pretrained=False, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
    """Constructs a ResNetV1d-50_8.8x model. Uses resnet50_v1d construction from resnetv1b.py

    Parameters
    ----------
    pretrained : bool or str
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    """
    model = ResNetV1b(BottleneckV1b, [3, 4, 6, 3], deep_stem=True, avg_down=True,
                      name_prefix='resnetv1d_', **kwargs)

    from .model_store import get_model_file
    params_file = get_model_file('resnet%d_v%dd_%.1fx' % (50, 1, 8.8), tag=pretrained, root=root)
    prune_gluon_block(model, model.name, ndarray.load(params_file), pretrained=pretrained, ctx=ctx)

    if pretrained:
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        model.synset = attrib.synset
        model.classes = attrib.classes
        model.classes_long = attrib.classes_long
    return model


def resnet101_v1d_1_point_9x(pretrained=False, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
    """Constructs a ResNetV1d-101_1.9x model. Uses resnet101_v1d construction from resnetv1b.py

    Parameters
    ----------
    pretrained : bool or str
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    """
    model = ResNetV1b(BottleneckV1b, [3, 4, 23, 3], deep_stem=True, avg_down=True,
                      name_prefix='resnetv1d_', **kwargs)

    from .model_store import get_model_file
    params_file = get_model_file('resnet%d_v%dd_%.1fx' % (101, 1, 1.9), tag=pretrained, root=root)
    prune_gluon_block(model, model.name, ndarray.load(params_file), pretrained=pretrained, ctx=ctx)

    if pretrained:
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        model.synset = attrib.synset
        model.classes = attrib.classes
        model.classes_long = attrib.classes_long
    return model


def resnet101_v1d_2_point_2x(pretrained=False, root='~/.mxnet/models', ctx=cpu(0), **kwargs):
    """Constructs a ResNetV1d-101_2.2x model. Uses resnet101_v1d construction from resnetv1b.py

    Parameters
    ----------
    pretrained : bool or str
        Boolean value controls whether to load the default pretrained weights for model.
        String value represents the hashtag for a certain version of pretrained weights.
    root : str, default '~/.mxnet/models'
        Location for keeping the model parameters.
    ctx : Context, default CPU
        The context in which to load the pretrained weights.
    """
    model = ResNetV1b(BottleneckV1b, [3, 4, 23, 3], deep_stem=True, avg_down=True,
                      name_prefix='resnetv1d_', **kwargs)

    from .model_store import get_model_file
    params_file = get_model_file('resnet%d_v%dd_%.1fx' % (101, 1, 2.2), tag=pretrained, root=root)
    prune_gluon_block(model, model.name, ndarray.load(params_file), pretrained=pretrained, ctx=ctx)

    if pretrained:
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        model.synset = attrib.synset
        model.classes = attrib.classes
        model.classes_long = attrib.classes_long
    return model