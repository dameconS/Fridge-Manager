import cv2
import imutils
from imutils.perspective import four_point_transform
import prrocr
import re

def ocr():
    image_path = "app/receipt/receipt.jpg"

    original_img = cv2.imread(image_path)
    # cv2.imshow("original image", original_img)

    if original_img is None:
        print("original_img is None")
        return "original_img is None"

    image = original_img.copy()
    image = imutils.resize(image, width=500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    receiptCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            receiptCnt = approx
            break

    if receiptCnt is None:
        raise Exception(("Could not find outline"))
        
    output = image.copy()
    cv2.drawContours(output, [receiptCnt], -1, (255, 0, 0), 3)

    ratio = original_img.shape[1] / float(image.shape[1])
    receipt = four_point_transform(original_img, receiptCnt.reshape(4, 2) * ratio)

    ocr = prrocr.ocr(lang="ko")
    result = ocr(receipt)

    if len(result) == 0:
        result = ocr(original_img)

    if isinstance(result, list):
        result = ' '.join(result)

    pattern = r'\d{2}[#*]?\s*([^\d]+?)\s+\d+,\s*\d+'

    items = re.findall(pattern, result)
    cleaned_items = [re.sub(r'[^\w가-힣\s]', '', item).strip() for item in items]
    
    return cleaned_items