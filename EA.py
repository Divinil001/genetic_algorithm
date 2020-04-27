import sys
import time
from copy import deepcopy

import numpy as np
from PIL import Image, ImageDraw, ImageChops


# Fitness function using RMSD
def fitness_function(image):
    rms = ImageChops.difference(image, input_image)
    histogram = rms.histogram()
    squares = (value * ((index % 256) ** 2) for index, value in enumerate(histogram))
    squares_sum = sum(squares)
    return squares_sum / float(width * height)


# Mutation function
def mutation(image):
    draw = ImageDraw.Draw(image)

    # Getting 3 random point's coordinates
    x = np.random.randint(0, height, 3)
    y = np.random.randint(0, width, 3)

    # Getting random colour without transparency
    colour = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256), 255)

    # Drawing it on the image
    draw.polygon([(x[0], y[0]), (x[1], y[1]), (x[2], y[2])], fill=colour, outline=colour)
    return image


# Main function
def main():
    start_time = time.time()

    # Creating "blank" image
    blank_image = Image.new('RGBA', (width, height), (0, 0, 0, 255))

    # Filling initial population
    population = [deepcopy(blank_image) for i in range(size_of_population)]

    first_parent = None
    second_parent = None

    # Starting generations
    for i in range(num_generations):
        first_best = sys.float_info.max
        second_best = sys.float_info.max

        # Finding two best individuals
        for individual in population:
            current_fitness = fitness_function(individual)

            if first_parent is None or current_fitness <= first_best:
                second_parent = first_parent
                first_parent = individual

                second_best = first_best
                first_best = current_fitness
            elif second_parent is None or current_fitness <= second_best:
                second_parent = individual
                second_best = current_fitness

        # Clearing population with saving "parents"
        population = [first_parent, second_parent]

        # Blending those images
        blend = Image.blend(first_parent, second_parent, 0.5)

        # Generating new population via mutation
        for j in range(size_of_population-2):
            population.append(mutation(deepcopy(blend)))

        # Saving intermediate results
        if i % 100 == 0:
            if inter_res:
                first_parent.save('output_{}_{}.png'.format(output_name, i // 100))
            print('Generation: ' + str(i))
            print('{}'.format(round(time.time()-start_time, 2)))

            # Stop if already good enough
            if first_best < satisfying_fitness:
                return

    # Saving the result
    first_parent.save('output_{}.png')
    print('Finished\n{}'.format(round(time.time()-start_time, 2)))


if __name__ == "__main__":
    # Size of population
    size_of_population = 25
    
    # Number of generations
    num_generations = 5000

    # Satisfying result of the fitness function
    satisfying_fitness = 1000

    # Change to 0 if you don't want to save intermidiate results
    inter_res = 1

    # Path to an image
    image_path = '/home/egor/Documents/[AI] Homework 2/alena.png'

    # Depending on platform getting the name of the file
    #   used in output filenames
    if sys.platform.startswith('win'):
        output_name = image_path.split('\\')[-1].split('.')[0]
    else:
        output_name = image_path.split('/')[-1].split('.')[0]

    # Trying to open the image
    try:
        input_image = Image.open(image_path).convert('RGBA')
    except IOError:
        print('Error 404\nCannot find an image\n')
        sys.exit(1)

    # Getting its width and height
    width, height = input_image.size
    print(width, height)

    main()
