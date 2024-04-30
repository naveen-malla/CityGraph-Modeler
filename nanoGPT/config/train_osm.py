

out_dir = 'out-osm'
eval_interval = 250 # keep frequent because we'll overfit
eval_iters = 200
log_interval = 10 # don't print too too often

always_save_checkpoint = True

wandb_log = False # override via command line if you like
wandb_project = 'osm'
wandb_run_name = 'osm-gpt'

dataset = 'osm'
gradient_accumulation_steps = 1
batch_size = 32
block_size = 1024

n_layer = 12
n_head = 12
n_embd = 768
dropout = 0.0

learning_rate = 1e-4 
max_iters = 20000
lr_decay_iters = 20000 # make equal to max_iters usually
min_lr = 1e-5 # learning_rate / 10 usually
beta2 = 0.96 

warmup_iters = 100 

