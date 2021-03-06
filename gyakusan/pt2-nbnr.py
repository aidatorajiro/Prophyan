# nurinuri

import torchvision.models as models

import torch
import torch.utils.data
import torchvision
from torchvision import transforms as T

# -0.5 0.5, -0.5 0.5, 10 - 1000 log?, 0 - 0.05, 0 - 0.05, 0 - 0.05
def makecircle(shape, x, y, s, r, g, b):
    xpos = torch.linspace(-0.5, 0.5, shape[0]).repeat(shape[1], 1).cuda()
    ypos = torch.linspace(-0.5, 0.5, shape[1]).reshape(shape[1],1).repeat(1, shape[0]).cuda()
    out = ((xpos - x) ** 2 + (ypos - y) ** 2)
    out = torch.clamp(1 - out*s, min = 0)
    out = out * torch.Tensor([[[r, g, b]]]).T.cuda()
    return out

with torch.cuda.device(0):
    resnext50_32x4d = models.resnext50_32x4d(pretrained=True).cuda()
    w = 224
    mean = 0.4
    std = 0.2

    points = 1000

    params = torch.stack([
        torch.rand(points) - 0.5,
        torch.rand(points) - 0.5,
        90*torch.rand(points) + 10,
        torch.rand(points)*0.04,
        torch.rand(points)*0.04,
        torch.rand(points)*0.04,
    ]).T.cuda().requires_grad_()

    print(params.shape)

    criterion = torch.nn.MSELoss(reduction='sum').cuda()
    optimizer = torch.optim.Adam([params], lr=0.001)

    for i in range(1000):
        addd = torch.zeros((1, 3, w, w)).cuda()
        for p in params:
            addd += makecircle((w, w), p[0], p[1], p[2], p[3], p[4], p[5])
        rett = resnext50_32x4d(addd)
        if i == 0:
            torchvision.utils.save_image(addd, __file__ + ".s.png")
            classid = 123
        loss = -torch.softmax(rett, 1)[0, classid]
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(loss)

    torchvision.utils.save_image(addd, __file__ + ".e.png")
