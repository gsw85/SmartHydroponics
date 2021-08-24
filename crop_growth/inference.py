##General utilities
import torch
import cv2
import math
import pathlib
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as im


from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer

path = pathlib.Path(__file__).parent.resolve()

class CropGrowth:
    
    predictor = None

    def __init__(self):
        cfg = get_cfg()
        cfg.merge_from_file(str(path) + "/myconfig.yml") 
        cfg.MODEL.DEVICE='cpu'
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6
        cfg.MODEL.WEIGHTS = str(path) + "/model_final.pth"
        self.predictor = DefaultPredictor(cfg)

    def perform_plant_growth_prediction(self):

        image_name = 'image.jpg'
        im = cv2.imread(str(path) + '/' + image_name)

        outputs = self.predictor(im)

        pred_masks = outputs["instances"].pred_masks.to("cpu").numpy()
        categories = outputs["instances"].to("cpu").pred_classes.numpy()
        predicted_boxes = outputs["instances"].pred_boxes.tensor.to("cpu").numpy()
        scores = outputs["instances"].scores.to("cpu").numpy()
       

        masks = []
        for x in range(len(pred_masks)):
            
            mask_h = int(math.ceil(predicted_boxes[x][3] - predicted_boxes[x][1]))
            mask_w = int(math.ceil(predicted_boxes[x][2] - predicted_boxes[x][0]))

            temp_mask = np.zeros((mask_h, mask_w))

            for x_idx in range(int(predicted_boxes[x][1]), int(predicted_boxes[x][3])):
                for y_idx in range(int(predicted_boxes[x][0]), int(predicted_boxes[x][2])):
                    temp_mask[x_idx - int(predicted_boxes[x][1])][y_idx - int(predicted_boxes[x][0])] = pred_masks[x][x_idx, y_idx]
            masks.append(temp_mask)

        temp_masks = masks
        sum_pixel = []
        area_pixels = []

        for x in range(len(temp_masks)):
            sum_pixel.append(np.sum(temp_masks[x])) 
            area_pixels.append(sum_pixel[x] * 0.0015868)

        area_label = torch.Tensor(area_pixels)

        v = Visualizer(
                im[:, :, ::-1], 
                metadata=None, 
                scale=0.8,
                )

        mask_track = 0

        v.draw_instance_predictions(outputs["instances"].to("cpu"))

        for box in outputs["instances"].pred_boxes.to('cpu'):
            box[0] = box[0] + 180
            v.draw_text(str(area_label[mask_track].numpy()) + ' cm²', tuple(box[:2].numpy()))
            mask_track = mask_track + 1
            
        v = v.get_output()

        cv2.imwrite(str(path) + '/seg_image.jpg', v.get_image()[:, :, ::-1])

        print("Image saved at" + str(path) + '/seg_image.jpg')

        inf = ''
        for x in range(len(temp_masks)):
            if(categories[x] == 0):
                label = 'Lettuce'
            if  x == 0 :

                inf = label + "," + str(area_pixels[x]) + "," + str(scores[x])
            else:
                inf = inf + ':' + label + "," + str(area_pixels[x]) + "," + str(scores[x])

        return inf



