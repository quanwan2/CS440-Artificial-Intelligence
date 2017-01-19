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
                for i in range(28):
                    row = current_image[i]
                    for j in range(28):
                        char = row[j]
                        if char in ['+', '#']:
                            value = 1.0
                        else:
                            value = 0.0
                        if (i, j, value, _class) in feature_dict:
                            feature_dict[(i, j, value, _class)] += 1.0
                        else:
                        	feature_dict[(i, j, value, _class)] = 1.0
    ##### Smooth The Curve #####
    for class_index in range(10):
        prior_value = training_example_count[class_index] / 5000
        p_class.append(prior_value)
        for i in range(28):
            for j in range(28):
                if (i,j,1.0,class_index) not in feature_dict:
                    feature_dict[(i,j,1.0,class_index)] = k/(training_example_count[class_index]+k*V)
                else:
                    feature_dict[(i,j,1.0,class_index)] = (feature_dict[(i,j,1.0,class_index)]+k)/(training_example_count[class_index]+k*V)
                if (i,j,0.0,class_index) not in feature_dict:
                    feature_dict[(i,j,0.0,class_index)] = k/(training_example_count[class_index]+k*V)
                else:
                    feature_dict[(i,j,0.0,class_index)] = (feature_dict[(i,j,0.0,class_index)]+k)/(training_example_count[class_index]+k*V)


def read_test_file():
    with open(test_image_file, 'r') as in_image_file:
        with open(test_label_file, 'r') as in_label_file:
            image_contents = in_image_file.readlines()
            label_contents = in_label_file.readlines()
            test_labels = label_contents
            high_low_digits = np.zeros((10,4))
            for i in range(10):
                high_low_digits[i,1] = sys.maxint
                high_low_digits[i,3] = -sys.maxint
            # print high_low_digits
            predictions = []
            for image_index in range(1000):
                true_label = int(test_labels[image_index])
                result = math.log( p_class[true_label] )
                current_image = image_contents[28*image_index:28*(image_index+1)]
                # print current_image
                for i in range(28):
                    row = current_image[i]
                    for j in range(28):
                        char = row[j]
                        if char in ['+', '#']:
                            value = 1.0
                        else:
                            value = 0.0
                        result += ( math.log(feature_dict[i,j,value,true_label]) )
                
                if result > high_low_digits[true_label, 3]:
                    high_low_digits[true_label, 3] = result
                    high_low_digits[true_label, 2] = image_index

                if result < high_low_digits[true_label, 1]:
                    high_low_digits[true_label, 1] = result
                    high_low_digits[true_label, 0] = image_index
            print high_low_digits

            # for i in range(10):
            #     print i
            #     print "Lowest:"
            #     for k in range(28):
            #         print image_contents[28*int(high_low_digits[i,0]):28*(int(high_low_digits[i,0])+1)][k]
            #     print "Highest:"
            #     for k in range(28):
            #         print image_contents[28*int(high_low_digits[i,2]):28*(int(high_low_digits[i,2])+1)][k]



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
    read_test_file()

    # digits_count = []
    # for i in range(10):
    #     digits_count.append(confusion_mat[i,i])
    # digits_count /= test_labels_count
    # print "\nClassification rate for each digit:"
    # print np.around(digits_count, decimals=3)
    # print "\nAccuracy:"
    # print np.around(accuracy, decimals=3)
    # print "\nConfusion Matrix:"
    # print np.around(confusion_mat, decimals=3)

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
    # for i in range( len(ZEROS) ):
    #     for j in range(28):
    #         print ZEROS[i][j]
    
