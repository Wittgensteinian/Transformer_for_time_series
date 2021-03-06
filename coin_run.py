from run.run import RunCoin
SRC_LEN, TGT_LEN = 300, 10

config = dict(
    run_quick=False,
    window_len=SRC_LEN+TGT_LEN,
    stride=10,
    src_len=SRC_LEN,
    tgt_len=TGT_LEN,
    embedding_dim=32,
    nhead=16,
    num_layers=(2, 2),
    ts_embed='conv',
    pos_embed='fixed',
    batch_size=128,
    lr=5e-4,
    betas=(0.9, 0.98),
    sch_stepsize=10,
    sch_gamma=0.75,
    es_patience=5,
    n_epoch=50,
)

coin = RunCoin('transformer_for_time_series_coin_data', config, verbose=2, watch=False, checkpoint_path='checkpoints/coin')