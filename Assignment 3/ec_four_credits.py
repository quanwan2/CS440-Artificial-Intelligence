import sys
import numpy as np
import math
from copy import deepcopy
#import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Four confusion pairs: (5,3):12, (8,3):14, (7,9):14, (4,9):18


test_image_file = 'digitdata/testimages'
test_label_file = 'digitdata/testlabels'
train_image_file = 'digitdata/trainingimages'
train_label_file = 'digitdata/traininglabels'

feature_dict = {} # Key: (i,j, f, class); Value: # of times pixel (i,j) has value f in training examples from this class.
training_example_count = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] # Total # of training examples from each class.
p_class = []

confusion_mat = np.zeros( (10,10) )
test_labels_count = np.zeros(10)

##### After testing many possible values for k (0.1 to 10), the accuracy decreases as k becomes larger. 0.1 is the best one. #####
k = 0.1
V = 2.0

def read_train_file():
    with open(train_image_file, 'r') as in_image_file:
        with open(train_label_file, 'r') as in_label_file:
            image_contents = in_image_file.readlines()
            label_contents = in_label_file.readlines()
            
            for image_index in range(5000):
                _class = int(label_contents[image_index])
                training_example_count[_class] += 1
                current_image = image_contents[28*image_index:28*(image_index+1)]
                for i in range(25):
                    for j in range(25):
                        p = ""
                        for m in range(4):
                            for n in range(4):
                                char = current_image[i+m][j+n]
                                if char in ['+', '#']:
                                    value = 1.0
                                else:
                                    value = 0.0
                                p += str( int(value) )
                        p = int(p, 2)
                        if (i, j, p, _class) in feature_dict:
                            feature_dict[(i, j, p, _class)] += 1.0
                        else:
                        	feature_dict[(i, j, p, _class)] = 1.0

    ##### Smooth The Curve #####
    for class_index in range(10):
        prior_value = training_example_count[class_index] / 5000
        p_class.append(prior_value)
        for i in range(25):
            for j in range(25):
                for val in range(65536):
                    # print (i,j,val,class_index)
                    if (i,j,val,class_index) not in feature_dict:
                        feature_dict[(i,j,val,class_index)] = k/(training_example_count[class_index]+k*V)
                    else:
                        feature_dict[(i,j,val,class_index)] = (feature_dict[(i,j,val,class_index)]+k)/(training_example_count[class_index]+k*V)


def read_test_file():
    with open(test_image_file, 'r') as in_image_file:
        with open(test_label_file, 'r') as in_label_file:
            image_contents = in_image_file.readlines()
            label_contents = in_label_file.readlines()
            test_labels = label_contents
            # high_low_digits = np.zeros((10,4))
            # for i in range(10):
            #     high_low_digits[i,1] = sys.maxint
            #     high_low_digits[i,3] = -sys.maxint
            # print high_low_digits
            predictions = []
            for image_index in range(1000):
                true_label = int(test_labels[image_index])
                results = 1.0*np.zeros(10)
                for k in range(10):
                    results[k] += math.log( p_class[k] )
                current_image = image_contents[28*image_index:28*(image_index+1)]
                # print current_image
                for i in range(25):
                    for j in range(25):
                        p = ""
                        for m in range(4):
                            for n in range(4):
                                char = current_image[i+m][j+n]
                                if char in ['+', '#']:
                                    value = 1.0
                                else:
                                    value = 0.0
                                p += str( int(value) )
                        p = int(p, 2)
                        for k in range(10):
                            results[k] += ( math.log(feature_dict[i,j,p,k]) )
                prediction = None
                tmp = -10**10
                for m in range(10):
                    if results[m] > tmp:
                        tmp = results[m]
                        prediction = m
                predictions.append(prediction)
            accuracy = accuracy_calculation(predictions,test_labels)
            return accuracy



def accuracy_calculation(predictions, test_labels):
    correct = 0.0
    for i in range(1000):
        confusion_mat[ int(test_labels[i]),predictions[i] ] += 1
        test_labels_count[int(test_labels[i])] += 1
        if predictions[i] == int(test_labels[i]):
            correct += 1.0
    # print correct
    for k in range(10):
        confusion_mat[k] /= test_labels_count[k]
    # print test_labels_count
    return correct/1000





def main():
    read_train_file()
    accuracy = read_test_file()

    digits_count = []
    for i in range(10):
        digits_count.append(confusion_mat[i,i])
    print "\nClassification rate for each digit:"
    print np.around(digits_count, decimals=3)
    print "\nAccuracy:"
    print np.around(accuracy, decimals=3)
    print "\nConfusion Matrix:"
    print np.around(confusion_mat, decimals=3)
    return
    # one_likehood = np.zeros( (28,28) )
    # three_likehood = np.zeros( (28,28) )
    # four_likehood = np.zeros( (28,28) )
    # five_likehood = np.zeros( (28,28) )
    # seven_likehood = np.zeros( (28,28) )
    # eight_likehood = np.zeros( (28,28) )
    # nine_likehood = np.zeros( (28,28) )
    # five_three_ratio = np.zeros( (28,28) )
    # eight_three_ratio = np.zeros( (28,28) )
    # seven_nine_ratio = np.zeros( (28,28) )
    # four_nine_ratio = np.zeros( (28,28) )
    # one_eight_ratio = np.zeros( (28,28) )

    # for i in range(28):
    #     for j in range(28):
    #         three_likehood[i,j] = math.log(feature_dict[i,j,1.0,3])
    #         four_likehood[i,j] = math.log(feature_dict[i,j,1.0,4])
    #         five_likehood[i,j] = math.log(feature_dict[i,j,1.0,5])
    #         seven_likehood[i,j] = math.log(feature_dict[i,j,1.0,7])
    #         eight_likehood[i,j] = math.log(feature_dict[i,j,1.0,8])
    #         nine_likehood[i,j] = math.log(feature_dict[i,j,1.0,9])
    #         one_likehood[i,j] = math.log(feature_dict[i,j,1.0,1])

    #         five_three_ratio[i,j] = math.log( feature_dict[i,j,1.0,5]/feature_dict[i,j,1.0,3] )
    #         eight_three_ratio[i,j] = math.log( feature_dict[i,j,1.0,8]/feature_dict[i,j,1.0,3] )
    #         seven_nine_ratio[i,j] = math.log( feature_dict[i,j,1.0,7]/feature_dict[i,j,1.0,9] )
    #         four_nine_ratio[i,j] = math.log( feature_dict[i,j,1.0,4]/feature_dict[i,j,1.0,9] )
    #         one_eight_ratio[i,j] = math.log( feature_dict[i,j,1.0,8]/feature_dict[i,j,1.0,1] )
  
    # plt.figure()
    # # plt.imshow(one_likehood)
    # # plt.imshow(four_likehood)
    # # plt.imshow(five_likehood)
    # # plt.imshow(seven_likehood)
    # # plt.imshow(eight_likehood)
    # plt.imshow(one_eight_ratio)
    # plt.colorbar()
    # plt.show()



if __name__ == "__main__":
    # print type(A)
    main()