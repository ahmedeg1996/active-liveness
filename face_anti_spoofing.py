import random 
import cv2
import imutils
import f_liveness_detection
import questions

cv2.namedWindow('liveness_detection')
cam = cv2.VideoCapture(0)

# parameters 
COUNTER, TOTAL = 0,0
counter_ok_questions = 0
counter_ok_consecutives = 0
limit_consecutives = 1 #parameter used to set the number of consecutive successful attempts required to move on to the next question during the liveness detection test
limit_questions = 3
counter_try = 0
limit_try = 40 #this is the time needed for the user to perform the question task.
# used_indices = []
question_order = [0, 2, 1]




def show_image(cam,text,color = (0,0,255)):
    ret, im = cam.read()
    im = imutils.resize(im, width=720)
    #im = cv2.flip(im, 1)
    cv2.putText(im,text,(10,50),cv2.FONT_HERSHEY_COMPLEX,1,color,2)
    return im


for index_question in question_order:
    question = questions.question_bank(index_question)

# for i_questions in range(0, limit_questions):
#     while True:
#         index_question = random.randint(0, limit_questions-1)
#         if index_question not in used_indices:
#             used_indices.append(index_question)
#             break
    
    question = questions.question_bank(index_question)
    
    im = show_image(cam,question)
    cv2.imshow('liveness_detection',im)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break 

    for i_try in range(limit_try):
        ret, im = cam.read()
        im = imutils.resize(im, width=720)
        im = cv2.flip(im, 1)
        TOTAL_0 = TOTAL
        out_model = f_liveness_detection.detect_liveness(im,COUNTER,TOTAL_0)
        # print(out_model)
        TOTAL = out_model['total_blinks']
        COUNTER = out_model['count_blinks_consecutives']
        dif_blink = TOTAL-TOTAL_0
        # print(dif_blink)
        if dif_blink > 0:
            blinks_up = 1
        else:
            blinks_up = 0

        challenge_res = questions.challenge_result(question, out_model,blinks_up)
        print(challenge_res)

        im = show_image(cam,question)
        cv2.imshow('liveness_detection',im)
        if cv2.waitKey(1) &0xFF == ord('q'):
            break 

        if challenge_res == "pass":
            im = show_image(cam,question+" : ok")
            cv2.imshow('liveness_detection',im)
            if cv2.waitKey(1) &0xFF == ord('q'):
                break
            print(counter_ok_consecutives)
            counter_ok_consecutives += 1
            if counter_ok_consecutives == limit_consecutives:
                counter_ok_questions += 1
                counter_try = 0
                counter_ok_consecutives = 0
                break
            else:
                continue

        elif challenge_res == "fail":
            counter_try += 1
            show_image(cam,question+" : fail")
        elif i_try == limit_try-1:
            break
            

    if counter_ok_questions ==  limit_questions:
        while True:
            im = show_image(cam,"LIFENESS SUCCESSFUL",color = (0,255,0))
            cv2.imshow('liveness_detection',im)
            if cv2.waitKey(1) &0xFF == ord('q'):
                break
    elif i_try == limit_try-1:
        while True:
            im = show_image(cam,"LIFENESS FAIL")
            cv2.imshow('liveness_detection',im)
            if cv2.waitKey(1) &0xFF == ord('q'):
                break
        break 

    else:
        continue
