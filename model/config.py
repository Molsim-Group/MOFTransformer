from sacred import Experiment

ex = Experiment("pretrained_mof")


def _loss_names(d):
    ret = {
        "ggm": 0,  # graph grid matching
        "mpp": 0,  # masked patch prediction
        "classification": 0,  # classification
        "regression": 0,  # regression
    }
    ret.update(d)
    return ret


@ex.config
def config():
    """
    # prepare_data
    max_num_atoms = 1000
    min_length = 30
    max_length = 60
    radius = 8
    max_nbr_atoms = 12
    """

    # model
    exp_name = "pretrained_mof"
    seed = 0
    use_cgcnn = False  # use CGCNN (crystal graph CNN)
    use_egcnn = False  # use EGCNN (energy grid CNN)
    use_transformer = False  # use graph embedding + vision transformer 3D
    loss_names = _loss_names({})

    # cgcnn
    n_conv = 5  # default of CGCNN=3
    atom_fea_len = 64  # default of CGCNN=64
    nbr_fea_len = 41  # dim for gaussian basis expansion

    # egcnn
    egcnn_depth = 18  # 10, 18, 34, 50, 101, 152, 200

    # cgcnn + egcnn
    strategy = 'concat'

    # graph seeting
    max_atom_len = 1000  # number of maximum atoms in primitive cell
    max_graph_len = 200  # number of maximum nodes in graph

    # grid setting
    img_size = 60
    patch_size = 10  # length of patch
    in_chans = 1  # channels of grid image
    max_grid_len = -1  # when -1, max_image_len is set to maximum ph*pw of batch images
    draw_false_grid = True

    # transformer setting
    hid_dim = 768
    num_heads = 12
    num_layers = 12
    mlp_ratio = 4
    drop_rate = 0.1
    mpp_ratio = 0.15

    # downstream
    downstream = ""
    n_classes = 0

    # Optimizer Setting
    optim_type = "adamw"  # adamw, adam, sgd (momentum=0.9)
    learning_rate = 1e-4
    weight_decay = 1e-2
    decay_power = 1  # or cosine
    max_epochs = 100
    max_steps = -1  # num_data * max_epoch // batch_size (accumulate_grad_batches)
    warmup_steps = 0.1  # int or float ( max_steps * warmup_steps)
    end_lr = 0
    lr_mult = 1  # multiply lr for downstream heads

    # PL Trainer Setting
    resume_from = None
    val_check_interval = 1.0
    test_only = False

    # below params varies with the environment
    data_root = ""
    log_dir = "result"
    batch_size = 256  # desired batch size; for gradient accumulation
    per_gpu_batchsize = 8  # you should define this manually with per_gpu_batch_size
    num_gpus = 2
    num_nodes = 1
    load_path = ""
    num_workers = 16  # the number of cpu's core
    precision = 16

    # experiments
    use_only_vit = False


"""
pretraining (ver 3)
"""


@ex.named_config
def task_topology_ver3():
    exp_name = "task_topology_ver3"
    data_root = "/home/data/pretrained_mof/ver3_unrelaxed/"
    downstream = "topology"
    log_dir = "result_ver3"

    # trainer
    max_epochs = 100
    batch_size = 1024
    per_gpu_batchsize = 16
    warmup_steps = 0.05

    # model
    use_only_vit = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 1120


@ex.named_config
def task_mpp_ver3_with_pretrained():
    exp_name = "task_mpp_ver3_with_pretrained"
    data_root = "/home/data/pretrained_mof/ver3_unrelaxed/"
    downstream = "topology"
    log_dir = "result_ver3"
    load_path = "/home/hspark8/PycharmProjects/pretrained_mof/result_ver3/task_topology_ver3_seed0_from_/best.ckpt"

    # trainer
    max_epochs = 100
    batch_size = 1024
    per_gpu_batchsize = 16
    warmup_steps = 0.05

    # model
    use_only_vit = True
    loss_names = _loss_names({"mpp": 1})


@ex.named_config
def task_mpp_ver3_without_pretrained():
    exp_name = "task_mpp_ver3_without_pretrained"
    data_root = "/home/data/pretrained_mof/ver3_unrelaxed/"
    downstream = "topology"
    log_dir = "result_ver3"

    # trainer
    max_epochs = 100
    batch_size = 1024
    per_gpu_batchsize = 16
    warmup_steps = 0.05

    # model
    use_only_vit = True
    loss_names = _loss_names({"mpp": 1})


@ex.named_config
def task_mpp_ver3_small_patch():
    exp_name = "task_mpp_ver3_small_patch"
    data_root = "/home/data/pretrained_mof/ver3_unrelaxed/"
    downstream = "topology"
    log_dir = "result_ver3"

    # trainer
    patch_size = 5
    max_grid_len = 200

    max_epochs = 100
    batch_size = 1024
    per_gpu_batchsize = 16
    warmup_steps = 0.05

    # model
    use_only_vit = True
    loss_names = _loss_names({"mpp": 1})


@ex.named_config
def task_mpp_ver3_interpolate():
    exp_name = "task_mpp_ver3_interpolate"
    data_root = "/home/data/pretrained_mof/ver3_unrelaxed/"
    downstream = "topology"
    log_dir = "result_ver3"

    # trainer
    max_epochs = 100
    batch_size = 1024
    per_gpu_batchsize = 16
    warmup_steps = 0.05

    # model
    use_only_vit = True
    loss_names = _loss_names({"mpp": 1})

    img_size = 30
    patch_size = 5
    draw_false_grid = False


@ex.named_config
def task_mpp_ver3_interpolate_mppratio():
    exp_name = "task_mpp_ver3_interpolate_mppratio"
    data_root = "/home/data/pretrained_mof/ver3_unrelaxed/"
    downstream = "topology"
    log_dir = "result_ver3"

    # trainer
    max_epochs = 100
    batch_size = 1024
    per_gpu_batchsize = 16
    warmup_steps = 0.05

    # model
    use_only_vit = True
    loss_names = _loss_names({"mpp": 1})

    img_size = 30
    patch_size = 5
    draw_false_grid = False
    mpp_ratio = 0.5


"""
pretraining (ver 2)
"""


@ex.named_config
def task_ggm_mpp():
    exp_name = "task_ggm_mpp"
    data_root = "/home/data/pretrained_mof/ver2/dataset/100k/"

    # model
    use_transformer = True
    loss_names = _loss_names({"ggm": 1, "mpp": 1})


"""
finetuning (ver2) - topology
"""


@ex.named_config
def task_topology_1k():
    exp_name = "task_topology_1k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/1k/"
    downstream = "topology"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 32

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def task_topology_10k():
    exp_name = "task_topology_10k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/10k/"
    downstream = "topology"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def task_topology_15k():
    exp_name = "task_topology_15k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/15k/"
    downstream = "topology"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


"""
finetuning (ver2) - cgmc
"""


@ex.named_config
def task_gcmc_1k():
    exp_name = "task_gcmc_1k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/1k/"
    downstream = "gcmc_h2_scaled_5bar"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"regression": 1})
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 32

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def task_gcmc_10k():
    exp_name = "task_gcmc_10k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/10k/"
    downstream = "gcmc_h2_scaled_5bar"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"regression": 1})
    draw_false_grid = False

    # trainer
    max_epochs = 100

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def task_gcmc_15k():
    exp_name = "task_gcmc_15k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/15k/"
    downstream = "gcmc_h2_scaled_5bar"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"regression": 1})
    draw_false_grid = False

    # trainer
    max_epochs = 100

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


"""
finetuning (ver2) - qmof
"""


@ex.named_config
def task_qmof_1k():
    exp_name = "task_qmof_1k"
    data_root = "/home/data/pretrained_mof/qmof_ver14/dataset/1k/"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"regression": 1})
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 32

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def task_qmof_10k():
    exp_name = "task_qmof_10k"
    data_root = "/home/data/pretrained_mof/qmof_ver14/dataset/10k/"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"regression": 1})
    draw_false_grid = False

    # trainer
    max_epochs = 100

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def task_qmof_15k():
    exp_name = "task_qmof_15k"
    data_root = "/home/data/pretrained_mof/qmof_ver14/dataset/15k/"
    load_path = "result/task_ggm_mpp_seed0_from_/version_0/checkpoints/best.ckpt"

    # model
    use_transformer = True
    loss_names = _loss_names({"regression": 1})
    draw_false_grid = False

    # trainer
    max_epochs = 100

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


"""
topology classfication (ver 2, 1k)
"""


@ex.named_config
def cgcnn_topology_1k():
    exp_name = "cgcnn_topology_1k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/1k/"
    downstream = "topology"

    # model
    use_cgcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 32

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def egcnn_topology_1k():
    exp_name = "egcnn_topology_1k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/1k/"
    downstream = "topology"

    # model
    use_egcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 32

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def cgcnn_egcnn_topology_1k():
    exp_name = "cgcnn_egcnn_topology_1k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/1k/"
    downstream = "topology"

    # model
    use_cgcnn = True
    use_egcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 32

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


"""
topology classfication (ver 2, 10k)
"""


@ex.named_config
def cgcnn_topology_10k():
    exp_name = "cgcnn_topology_10k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/10k/"
    downstream = "topology"

    # model
    use_cgcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 256

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def egcnn_topology_10k():
    exp_name = "egcnn_topology_10k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/10k/"
    downstream = "topology"

    # model
    use_egcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 256

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def cgcnn_egcnn_topology_10k():
    exp_name = "cgcnn_egcnn_topology_10k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/10k/"
    downstream = "topology"

    # model
    use_cgcnn = True
    use_egcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 256

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


"""
topology classfication (ver 2, 100k)
"""


@ex.named_config
def cgcnn_topology_100k():
    exp_name = "cgcnn_topology_100k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/100k/"
    downstream = "topology"

    # model
    use_cgcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 256

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def egcnn_topology_100k():
    exp_name = "egcnn_topology_100k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/100k/"
    downstream = "topology"

    # model
    use_egcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 256

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.


@ex.named_config
def cgcnn_egcnn_topology_100k():
    exp_name = "cgcnn_egcnn_topology_100k"
    data_root = "/home/data/pretrained_mof/ver2/dataset/100k/"
    downstream = "topology"

    # model
    use_cgcnn = True
    use_egcnn = True
    loss_names = _loss_names({"classification": 1})
    n_classes = 300
    draw_false_grid = False

    # trainer
    max_epochs = 100
    batch_size = 256

    # optimizer
    optim_type = "sgd"
    learning_rate = 1e-2
    weight_decay = 0.
