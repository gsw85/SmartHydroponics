import io
import requests
import torch
import torchvision
import torchvision.transforms as T
import os
import json 
from PIL import Image, ImageDraw, ImageFont
from torchvision import models
from torch.autograd import Variable

import sys
sys.path.append(".")
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def classify():

    # Load weights from our trained model
    device = torch.device("cpu")
    model= torch.load(PROJECT_ROOT + '/transflearn.pt', map_location='cpu')
    model.eval()

    normalize = T.Normalize(
        mean = [0.485, 0.456, 0.406],
        std = [0.229, 0.224, 0.225]
    )
    preprocess = T.Compose([
        T.Resize(224),
        T.CenterCrop(224),
        T.ToTensor(),
        normalize
    ])

    # Read image from disk
    img_path = os.path.dirname(os.path.realpath(__file__)) + '/testImg/downymildewdisease (93).jpg'
    img_pil = Image.open(img_path)
    
    # Resize PIL image
    resized_img_pil = img_pil.resize((300,300))
    draw = ImageDraw.Draw(resized_img_pil)

    img_tensor = preprocess(img_pil)
    img_tensor.unsqueeze_(0)

    img_variable = Variable(img_tensor)
    img_variable = img_variable.to(device)
    fc_out = model(img_variable)

    with open(PROJECT_ROOT + "/classes.txt") as f:
        labels = [line.strip() for line in f.readlines()]

    _, index = torch.max(fc_out,1)
    percentage = torch.nn.functional.softmax(fc_out,dim=1)[0] * 100
    # print(labels[index[0]], percentage[index[0]].item())
    condplant = str(labels[index[0]])
    condperc = format(percentage[index[0]].item(),".2f")
    print("Condition: " + condplant)
    print("Percentage: " + condperc)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
    draw.text((5, 0), "Condition: " + condplant, (255,255,255), font=font)
    draw.text((5, 30), "Probability: " + condperc, (255,255,255), font=font)
    resized_img_pil.show()
    resized_img_pil.save(PROJECT_ROOT + "/cfm.jpg")

# if __name__ == '__main__':
#     classify()

