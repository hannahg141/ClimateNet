import torch
from torch.autograd import Variable
from torch import nn
import numpy as np
import torch.nn.functional as F

def jaccard_loss(logits, true, eps=1e-7):
    """Computes the Jaccard loss, a.k.a the IoU loss.
    Note that PyTorch optimizers minimize a loss. In this
    case, we would like to maximize the jaccard loss so we
    return the negated jaccard loss.
    Args:
        true: a tensor of shape [B, H, W] or [B, 1, H, W].
        logits: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or logits of the model.
        eps: added to the denominator for numerical stability.
    Returns:
        jacc_loss: the Jaccard loss.
    """
    num_classes = logits.shape[1]
    true_1_hot = torch.eye(num_classes)[true.squeeze(1)]
    true_1_hot = true_1_hot.permute(0, 3, 1, 2).float()
    probas = F.softmax(logits, dim=1)
    true_1_hot = true_1_hot.type(logits.type())
    dims = (0,) + tuple(range(2, true.ndimension()))
    intersection = torch.sum(probas * true_1_hot, dims)
    cardinality = torch.sum(probas + true_1_hot, dims)
    union = cardinality - intersection
    jacc_loss = (intersection / (union + eps)).mean()
    return (1 - jacc_loss)


def cross_entropy_loss(y_logit, y_true):
    '''
    Multi-label cross-entropy
    * Required "Wp", "Wn" as positive & negative class-weights
    y_true: true value
    y_logit: predicted value
    WIP
    '''
    # N = len(df) # 37993  // df is data frame need to sub out
    # labels = df.keys()[1:] # ['label_1', ...., 'label_6']
    #
    # for k, label in enumerate(sorted(labels)):
    #     positives = sum(df[label] == 1)
    #
    # class_weights = {}
    # positive_weights = {}
    # negative_weights = {}
    #
    # for label in sorted(labels):
    #     positive_weights[label] = N /(2 * sum(df[label] == 1))
    #     negative_weights[label] = N /(2 * sum(df[label] == 0))
    #
    # Wp = positive_weights
    # Wn = negative_weights

    loss = float(0)

    for i, key in enumerate(Wp.keys()):
        first_term = y_true[i] * torch.log(y_logit[i] + torch.epsilon())
        second_term = (1 - y_true[i]) * torch.log(1 - y_logit[i] + torch.epsilon())
        # first_term = Wp[key] * y_true[i] * K.log(y_logit[i] + K.epsilon())
        # second_term = Wn[key] * (1 - y_true[i]) * K.log(1 - y_logit[i] + K.epsilon())
        loss -= (first_term + second_term)
    return loss

def cross_entropy_loss_pytorch(y_logit, y_true):
    '''
    Multi-label cross-entropy with pytorch
    y_true: true value
    y_logit: predicted value
    https://www.cs.toronto.edu/~lczhang/321/tut/tut04.pdf
    https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
    '''


    loss = nn.CrossEntropyLoss()

    return loss(y_logit,y_true)