
# Models

## Results

We trained and report here the following models:

1. Baseline CGNet model (Jaccard loss, 15 epochs)
2. Baseline trained with learning rate scheduler
3. Model 2 trained on engineered features (velocity/vorticity)
4. Model 3 + cross-entropy loss 
5. Model 3 + weighted cross-entropy loss 
6. Model 3 + focal Tversky loss 
7. Model 3 + weighted Jaccard loss 

For each model, we provide:
- config.json: configuration file to load the model
- weights.pth: trained weights ready to use for predictions
- history.csv: complete training, validation and test metrics history


## Model Architecture

We provide **print.py**, a script that uses the Torchinfo package to print the details of the model layers architecture, size, and parameter counts.

Syntax:

```
$ print.py --model_path <model_path> -data_path <data_path> --level <level> 
$ print.py -m <model_path> -d <data_path> -l <level>

<model_path>: path to folder containing config.json describing the model 
<data_path>: path folder containing dataset with corresponding layers
<level>: int setting depth of detail of the output (1: high-level, 3: granular)
```

Reference: https://github.com/TylerYep/torchinfo


## CGNet Detailed Architecture

```
=================================================================================================================================================
Layer (type:depth-idx)                        Input Shape               Output Shape              Param #                   Mult-Adds
=================================================================================================================================================
CGNetModule                                   [4, 4, 768, 1152]         [4, 3, 768, 1152]         --                        --
├─ConvBNPReLU: 1-1                            [4, 4, 768, 1152]         [4, 32, 384, 576]         --                        --
│    └─Wrap: 2-1                              [4, 4, 768, 1152]         [4, 4, 770, 1154]         --                        --
│    └─Conv2d: 2-2                            [4, 4, 770, 1154]         [4, 32, 384, 576]         1,152                     1,019,215,872
│    └─BatchNorm2d: 2-3                       [4, 32, 384, 576]         [4, 32, 384, 576]         64                        256
│    └─PReLU: 2-4                             [4, 32, 384, 576]         [4, 32, 384, 576]         32                        128
├─ConvBNPReLU: 1-2                            [4, 32, 384, 576]         [4, 32, 384, 576]         --                        --
│    └─Wrap: 2-5                              [4, 32, 384, 576]         [4, 32, 386, 578]         --                        --
│    └─Conv2d: 2-6                            [4, 32, 386, 578]         [4, 32, 384, 576]         9,216                     8,153,726,976
│    └─BatchNorm2d: 2-7                       [4, 32, 384, 576]         [4, 32, 384, 576]         64                        256
│    └─PReLU: 2-8                             [4, 32, 384, 576]         [4, 32, 384, 576]         32                        128
├─ConvBNPReLU: 1-3                            [4, 32, 384, 576]         [4, 32, 384, 576]         --                        --
│    └─Wrap: 2-9                              [4, 32, 384, 576]         [4, 32, 386, 578]         --                        --
│    └─Conv2d: 2-10                           [4, 32, 386, 578]         [4, 32, 384, 576]         9,216                     8,153,726,976
│    └─BatchNorm2d: 2-11                      [4, 32, 384, 576]         [4, 32, 384, 576]         64                        256
│    └─PReLU: 2-12                            [4, 32, 384, 576]         [4, 32, 384, 576]         32                        128
├─InputInjection: 1-4                         [4, 4, 768, 1152]         [4, 4, 384, 576]          --                        --
│    └─ModuleList: 2-13                       --                        --                        --                        --
│    │    └─Wrap: 3-1                         [4, 4, 768, 1152]         [4, 4, 770, 1154]         --                        --
│    │    └─AvgPool2d: 3-2                    [4, 4, 770, 1154]         [4, 4, 384, 576]          --                        --
├─InputInjection: 1-5                         [4, 4, 768, 1152]         [4, 4, 192, 288]          --                        --
│    └─ModuleList: 2-14                       --                        --                        --                        --
│    │    └─Wrap: 3-3                         [4, 4, 768, 1152]         [4, 4, 770, 1154]         --                        --
│    │    └─AvgPool2d: 3-4                    [4, 4, 770, 1154]         [4, 4, 384, 576]          --                        --
│    │    └─Wrap: 3-5                         [4, 4, 384, 576]          [4, 4, 386, 578]          --                        --
│    │    └─AvgPool2d: 3-6                    [4, 4, 386, 578]          [4, 4, 192, 288]          --                        --
├─BNPReLU: 1-6                                [4, 36, 384, 576]         [4, 36, 384, 576]         --                        --
│    └─BatchNorm2d: 2-15                      [4, 36, 384, 576]         [4, 36, 384, 576]         72                        288
│    └─PReLU: 2-16                            [4, 36, 384, 576]         [4, 36, 384, 576]         36                        144
├─ContextGuidedBlock_Down: 1-7                [4, 36, 384, 576]         [4, 64, 192, 288]         --                        --
│    └─ConvBNPReLU: 2-17                      [4, 36, 384, 576]         [4, 64, 192, 288]         --                        --
│    │    └─Wrap: 3-7                         [4, 36, 384, 576]         [4, 36, 386, 578]         --                        --
│    │    └─Conv2d: 3-8                       [4, 36, 386, 578]         [4, 64, 192, 288]         20,736                    4,586,471,424
│    │    └─BatchNorm2d: 3-9                  [4, 64, 192, 288]         [4, 64, 192, 288]         128                       512
│    │    └─PReLU: 3-10                       [4, 64, 192, 288]         [4, 64, 192, 288]         64                        256
│    └─ChannelWiseConv: 2-18                  [4, 64, 192, 288]         [4, 64, 192, 288]         --                        --
│    │    └─Wrap: 3-11                        [4, 64, 192, 288]         [4, 64, 194, 290]         --                        --
│    │    └─Conv2d: 3-12                      [4, 64, 194, 290]         [4, 64, 192, 288]         576                       127,401,984
│    └─ChannelWiseDilatedConv: 2-19           [4, 64, 192, 288]         [4, 64, 192, 288]         --                        --
│    │    └─Wrap: 3-13                        [4, 64, 192, 288]         [4, 64, 196, 292]         --                        --
│    │    └─Conv2d: 3-14                      [4, 64, 196, 292]         [4, 64, 192, 288]         576                       127,401,984
│    └─BatchNorm2d: 2-20                      [4, 128, 192, 288]        [4, 128, 192, 288]        256                       1,024
│    └─PReLU: 2-21                            [4, 128, 192, 288]        [4, 128, 192, 288]        128                       512
│    └─Conv: 2-22                             [4, 128, 192, 288]        [4, 64, 192, 288]         --                        --
│    │    └─Wrap: 3-15                        [4, 128, 192, 288]        [4, 128, 192, 288]        --                        --
│    │    └─Conv2d: 3-16                      [4, 128, 192, 288]        [4, 64, 192, 288]         8,192                     1,811,939,328
│    └─FGlo: 2-23                             [4, 64, 192, 288]         [4, 64, 192, 288]         --                        --
│    │    └─AdaptiveAvgPool2d: 3-17           [4, 64, 192, 288]         [4, 64, 1, 1]             --                        --
│    │    └─Sequential: 3-18                  [4, 64]                   [4, 64]                   1,096                     4,384
├─ModuleList: 1-8                             --                        --                        --                        --
│    └─ContextGuidedBlock: 2-24               [4, 64, 192, 288]         [4, 64, 192, 288]         --                        --
│    │    └─ConvBNPReLU: 3-19                 [4, 64, 192, 288]         [4, 32, 192, 288]         2,144                     452,985,216
│    │    └─ChannelWiseConv: 3-20             [4, 32, 192, 288]         [4, 32, 192, 288]         288                       63,700,992
│    │    └─ChannelWiseDilatedConv: 3-21      [4, 32, 192, 288]         [4, 32, 192, 288]         288                       63,700,992
│    │    └─BNPReLU: 3-22                     [4, 64, 192, 288]         [4, 64, 192, 288]         192                       768
│    │    └─FGlo: 3-23                        [4, 64, 192, 288]         [4, 64, 192, 288]         1,096                     4,384
│    └─ContextGuidedBlock: 2-25               [4, 64, 192, 288]         [4, 64, 192, 288]         --                        --
│    │    └─ConvBNPReLU: 3-24                 [4, 64, 192, 288]         [4, 32, 192, 288]         2,144                     452,985,216
│    │    └─ChannelWiseConv: 3-25             [4, 32, 192, 288]         [4, 32, 192, 288]         288                       63,700,992
│    │    └─ChannelWiseDilatedConv: 3-26      [4, 32, 192, 288]         [4, 32, 192, 288]         288                       63,700,992
│    │    └─BNPReLU: 3-27                     [4, 64, 192, 288]         [4, 64, 192, 288]         192                       768
│    │    └─FGlo: 3-28                        [4, 64, 192, 288]         [4, 64, 192, 288]         1,096                     4,384
├─BNPReLU: 1-9                                [4, 132, 192, 288]        [4, 132, 192, 288]        --                        --
│    └─BatchNorm2d: 2-26                      [4, 132, 192, 288]        [4, 132, 192, 288]        264                       1,056
│    └─PReLU: 2-27                            [4, 132, 192, 288]        [4, 132, 192, 288]        132                       528
├─ContextGuidedBlock_Down: 1-10               [4, 132, 192, 288]        [4, 128, 96, 144]         --                        --
│    └─ConvBNPReLU: 2-28                      [4, 132, 192, 288]        [4, 128, 96, 144]         --                        --
│    │    └─Wrap: 3-29                        [4, 132, 192, 288]        [4, 132, 194, 290]        --                        --
│    │    └─Conv2d: 3-30                      [4, 132, 194, 290]        [4, 128, 96, 144]         152,064                   8,408,530,944
│    │    └─BatchNorm2d: 3-31                 [4, 128, 96, 144]         [4, 128, 96, 144]         256                       1,024
│    │    └─PReLU: 3-32                       [4, 128, 96, 144]         [4, 128, 96, 144]         128                       512
│    └─ChannelWiseConv: 2-29                  [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─Wrap: 3-33                        [4, 128, 96, 144]         [4, 128, 98, 146]         --                        --
│    │    └─Conv2d: 3-34                      [4, 128, 98, 146]         [4, 128, 96, 144]         1,152                     63,700,992
│    └─ChannelWiseDilatedConv: 2-30           [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─Wrap: 3-35                        [4, 128, 96, 144]         [4, 128, 104, 152]        --                        --
│    │    └─Conv2d: 3-36                      [4, 128, 104, 152]        [4, 128, 96, 144]         1,152                     63,700,992
│    └─BatchNorm2d: 2-31                      [4, 256, 96, 144]         [4, 256, 96, 144]         512                       2,048
│    └─PReLU: 2-32                            [4, 256, 96, 144]         [4, 256, 96, 144]         256                       1,024
│    └─Conv: 2-33                             [4, 256, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─Wrap: 3-37                        [4, 256, 96, 144]         [4, 256, 96, 144]         --                        --
│    │    └─Conv2d: 3-38                      [4, 256, 96, 144]         [4, 128, 96, 144]         32,768                    1,811,939,328
│    └─FGlo: 2-34                             [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─AdaptiveAvgPool2d: 3-39           [4, 128, 96, 144]         [4, 128, 1, 1]            --                        --
│    │    └─Sequential: 3-40                  [4, 128]                  [4, 128]                  2,184                     8,736
├─ModuleList: 1-11                            --                        --                        --                        --
│    └─ContextGuidedBlock: 2-35               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-41                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-42             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-43      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-44                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-45                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-36               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-46                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-47             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-48      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-49                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-50                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-37               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-51                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-52             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-53      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-54                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-55                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-38               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-56                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-57             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-58      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-59                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-60                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-39               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-61                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-62             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-63      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-64                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-65                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-40               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-66                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-67             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-68      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-69                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-70                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-41               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-71                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-72             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-73      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-74                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-75                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-42               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-76                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-77             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-78      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-79                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-80                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-43               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-81                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-82             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-83      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-84                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-85                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-44               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-86                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-87             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-88      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-89                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-90                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-45               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-91                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-92             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-93      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-94                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-95                        [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-46               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-96                 [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-97             [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-98      [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-99                     [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-100                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-47               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-101                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-102            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-103     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-104                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-105                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-48               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-106                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-107            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-108     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-109                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-110                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-49               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-111                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-112            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-113     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-114                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-115                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-50               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-116                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-117            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-118     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-119                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-120                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-51               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-121                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-122            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-123     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-124                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-125                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-52               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-126                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-127            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-128     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-129                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-130                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-53               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-131                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-132            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-133     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-134                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-135                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
│    └─ContextGuidedBlock: 2-54               [4, 128, 96, 144]         [4, 128, 96, 144]         --                        --
│    │    └─ConvBNPReLU: 3-136                [4, 128, 96, 144]         [4, 64, 96, 144]          8,384                     452,985,600
│    │    └─ChannelWiseConv: 3-137            [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─ChannelWiseDilatedConv: 3-138     [4, 64, 96, 144]          [4, 64, 96, 144]          576                       31,850,496
│    │    └─BNPReLU: 3-139                    [4, 128, 96, 144]         [4, 128, 96, 144]         384                       1,536
│    │    └─FGlo: 3-140                       [4, 128, 96, 144]         [4, 128, 96, 144]         2,184                     8,736
├─BNPReLU: 1-12                               [4, 256, 96, 144]         [4, 256, 96, 144]         --                        --
│    └─BatchNorm2d: 2-55                      [4, 256, 96, 144]         [4, 256, 96, 144]         512                       2,048
│    └─PReLU: 2-56                            [4, 256, 96, 144]         [4, 256, 96, 144]         256                       1,024
├─Sequential: 1-13                            [4, 256, 96, 144]         [4, 3, 96, 144]           --                        --
│    └─Conv: 2-57                             [4, 256, 96, 144]         [4, 3, 96, 144]           --                        --
│    │    └─Wrap: 3-141                       [4, 256, 96, 144]         [4, 256, 96, 144]         --                        --
│    │    └─Conv2d: 3-142                     [4, 256, 96, 144]         [4, 3, 96, 144]           768                       42,467,328
=================================================================================================================================================
Total params: 494,232
Trainable params: 494,232
Non-trainable params: 0
Total mult-adds (G): 45.86
=================================================================================================================================================
Input size (MB): 56.62
Forward/backward pass size (MB): 11057.09
Params size (MB): 1.98
Estimated Total Size (MB): 11115.69
=================================================================================================================================================
```