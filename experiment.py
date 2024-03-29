"""Problem Set 4: Motion Detection"""

import cv2
import os
import numpy as np

import ps4

# I/O directories
input_dir = "input_images"
output_dir = "./"


# Utility code
def quiver(u, v, scale, stride, color=(0, 255, 0)):

    img_out = np.zeros((v.shape[0], u.shape[1], 3), dtype=np.uint8)

    for y in range(0, v.shape[0], stride):

        for x in range(0, u.shape[1], stride):

            cv2.line(img_out, (x, y), (x + int(u[y, x] * scale),
                                       y + int(v[y, x] * scale)), color, 1)
            cv2.circle(img_out, (x + int(u[y, x] * scale),
                                 y + int(v[y, x] * scale)), 1, color, 1)
    return img_out


# Functions you need to complete:

def scale_u_and_v(u, v, level, pyr):
    """Scales up U and V arrays to match the image dimensions assigned
    to the first pyramid level: pyr[0].

    You will use this method in part 3. In this section you are asked
    to select a level in the gaussian pyramid which contains images
    that are smaller than the one located in pyr[0]. This function
    should take the U and V arrays computed from this lower level and
    expand them to match a the size of pyr[0].

    This function consists of a sequence of ps4.expand_image operations
    based on the pyramid level used to obtain both U and V. Multiply
    the result of expand_image by 2 to scale the vector values. After
    each expand_image operation you should adjust the resulting arrays
    to match the current level shape
    i.e. U.shape == pyr[current_level].shape and
    V.shape == pyr[current_level].shape. In case they don't, adjust
    the U and V arrays by removing the extra rows and columns.

    Hint: create a for loop from level-1 to 0 inclusive.

    Both resulting arrays' shapes should match pyr[0].shape.

    Args:
        u: U array obtained from ps4.optic_flow_lk
        v: V array obtained from ps4.optic_flow_lk
        level: level value used in the gaussian pyramid to obtain U
               and V (see part_3)
        pyr: gaussian pyramid used to verify the shapes of U and V at
             each iteration until the level 0 has been met.

    Returns:
        tuple: two-element tuple containing:
            u (numpy.array): scaled U array of shape equal to
                             pyr[0].shape
            v (numpy.array): scaled V array of shape equal to
                             pyr[0].shape
    """

    for _ in range(level):
        u = 2 * ps4.expand_image(u)
        v = 2 * ps4.expand_image(v)

    shape = pyr[0].shape
    return u[:shape[0], :shape[1]], v[:shape[0], :shape[1]]


def part_1a():

    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                      'Shift0.png'), 0) / 255.
    shift_r2 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                       'ShiftR2.png'), 0) / 255.
    shift_r5_u5 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                          'ShiftR5U5.png'), 0) / 255.

    # Optional: smooth the images if LK doesn't work well on raw images
    k_size = 27
    k_type = 'uniform'
    sigma = 0
    u, v = ps4.optic_flow_lk(shift_0, shift_r2, k_size, k_type, sigma)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-a-1.png"), u_v)

    # Now let's try with ShiftR5U5. You may want to try smoothing the
    # input images first.

    k_size = 65
    k_type = 'gaussian'
    sigma = 25

    gaussian_ksize = (7, 7)
    gaussian_sigma = 5
    smooth_shift_0 = cv2.GaussianBlur(shift_0, gaussian_ksize, gaussian_sigma)
    smooth_shift_r5_u5 = cv2.GaussianBlur(shift_r5_u5, gaussian_ksize, gaussian_sigma)

    u, v = ps4.optic_flow_lk(smooth_shift_0, smooth_shift_r5_u5, k_size, k_type, sigma)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-a-2.png"), u_v)


def part_1b():
    """Performs the same operations applied in part_1a using the images
    ShiftR10, ShiftR20 and ShiftR40.

    You will compare the base image Shift0.png with the remaining
    images located in the directory TestSeq:
    - ShiftR10.png
    - ShiftR20.png
    - ShiftR40.png

    Make sure you explore different parameters and/or pre-process the
    input images to improve your results.

    In this part you should save the following images:
    - ps4-1-b-1.png
    - ps4-1-b-2.png
    - ps4-1-b-3.png

    Returns:
        None
    """
    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                      'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR10.png'), 0) / 255.
    shift_r20 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR20.png'), 0) / 255.
    shift_r40 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR40.png'), 0) / 255.
    # =======
    # PART B1
    # =======

    gaussian_sigma = 5
    gaussian_ksize = (9, 9)

    s_shift_0 = cv2.GaussianBlur(shift_0, gaussian_ksize, gaussian_sigma)
    s_shift_r10 = cv2.GaussianBlur(shift_r10, gaussian_ksize, gaussian_sigma)

    k_size = 85
    k_type = 'gaussian'
    sigma = 30
    u, v = ps4.optic_flow_lk(s_shift_0, s_shift_r10, k_size, k_type, sigma)

    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-b-1.png"), u_v)

    # =======
    # PART B2
    # =======

    gaussian_sigma = 15
    gaussian_ksize = (27,27)
    s_shift_0 = np.copy(shift_0)
    s_shift_r20 = np.copy(shift_r20)
    s_shift_0 = cv2.GaussianBlur(shift_0, gaussian_ksize, gaussian_sigma)
    s_shift_r20 = cv2.GaussianBlur(shift_r20, gaussian_ksize, gaussian_sigma)

    k_size = 95
    k_type = 'uniform'
    sigma = 0
    u, v = ps4.optic_flow_lk(s_shift_0, s_shift_r20, k_size, k_type, sigma)

    gaussian_sigma = 25
    gaussian_ksize = (25, 25)
    u = cv2.GaussianBlur(u, gaussian_ksize, gaussian_sigma)
    v = cv2.GaussianBlur(v, gaussian_ksize, gaussian_sigma)

    u_v = quiver(u, v, scale=1, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-b-2.png"), u_v)

    # =======
    # PART B3
    # =======

    gaussian_sigma = 100
    gaussian_ksize = (55,55)
    s_shift_0 = np.copy(shift_0)
    s_shift_r40 = np.copy(shift_r40)
    s_shift_0 = cv2.GaussianBlur(shift_0, gaussian_ksize, gaussian_sigma)
    s_shift_r40 = cv2.GaussianBlur(shift_r40, gaussian_ksize, gaussian_sigma)

    k_size = 95
    k_type = 'uniform'
    sigma = 50
    u, v = ps4.optic_flow_lk(s_shift_0, s_shift_r40, k_size, k_type, sigma)

    gaussian_sigma = 40
    gaussian_ksize = (35, 35)
    u = cv2.GaussianBlur(u, gaussian_ksize, gaussian_sigma)
    v = cv2.GaussianBlur(v, gaussian_ksize, gaussian_sigma)

    # Flow image
    u_v = quiver(u, v, scale=0.4, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-b-3.png"), u_v)


def part_2():

    yos_img_01 = cv2.imread(os.path.join(input_dir, 'DataSeq1',
                                         'yos_img_01.jpg'), 0) / 255.

    # 2a
    levels = 4
    yos_img_01_g_pyr = ps4.gaussian_pyramid(yos_img_01, levels)
    yos_img_01_g_pyr_img = ps4.create_combined_img(yos_img_01_g_pyr)
    cv2.imwrite(os.path.join(output_dir, "ps4-2-a-1.png"),
                yos_img_01_g_pyr_img)

    # 2b
    yos_img_01_l_pyr = ps4.laplacian_pyramid(yos_img_01_g_pyr)

    yos_img_01_l_pyr_img = ps4.create_combined_img(yos_img_01_l_pyr)
    cv2.imwrite(os.path.join(output_dir, "ps4-2-b-1.png"),
                yos_img_01_l_pyr_img)


def part_3a_1():
    yos_img_01 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_01.jpg'), 0) / 255.
    yos_img_02 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_02.jpg'), 0) / 255.

    levels = 5  # Define the number of pyramid levels
    yos_img_01_g_pyr = ps4.gaussian_pyramid(yos_img_01, levels)
    yos_img_02_g_pyr = ps4.gaussian_pyramid(yos_img_02, levels)

    ps4.write_images(yos_img_01_g_pyr, 'part3')

    level_id = 1
    k_size = 15
    k_type = "uniform"
    sigma = 10
    u, v = ps4.optic_flow_lk(yos_img_01_g_pyr[level_id],
                             yos_img_02_g_pyr[level_id],
                             k_size, k_type, sigma)

    u, v = scale_u_and_v(u, v, level_id, yos_img_02_g_pyr)

    # TODO: Remove this
    # u_v = quiver(u, v, scale=7, stride=10)
    # cv2.imwrite(os.path.join(output_dir, "test1.png"), u_v)

    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values
    yos_img_02_warped = ps4.warp(yos_img_02, u, v, interpolation, border_mode)

    diff_yos_img = yos_img_01 - yos_img_02_warped
    cv2.imwrite(os.path.join(output_dir, "ps4-3-a-1.png"),
                ps4.normalize_and_scale(diff_yos_img))
    cv2.imwrite(os.path.join(output_dir, "res1.png"),
                ps4.normalize_and_scale(diff_yos_img))


def part_3a_2():
    yos_img_02 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_02.jpg'), 0) / 255.
    yos_img_03 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_03.jpg'), 0) / 255.

    levels = 3  # Define the number of pyramid levels
    yos_img_02_g_pyr = ps4.gaussian_pyramid(yos_img_02, levels)
    yos_img_03_g_pyr = ps4.gaussian_pyramid(yos_img_03, levels)

    level_id = 1
    k_size = 15
    k_type = 'uniform'
    sigma = 0
    u, v = ps4.optic_flow_lk(yos_img_02_g_pyr[level_id],
                             yos_img_03_g_pyr[level_id],
                             k_size, k_type, sigma)

    u, v = scale_u_and_v(u, v, level_id, yos_img_03_g_pyr)

    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values
    yos_img_03_warped = ps4.warp(yos_img_03, u, v, interpolation, border_mode)

    diff_yos_img = yos_img_02 - yos_img_03_warped
    cv2.imwrite(os.path.join(output_dir, "ps4-3-a-2.png"),
                ps4.normalize_and_scale(diff_yos_img))


def part_4a():
    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                      'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR10.png'), 0) / 255.
    shift_r20 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR20.png'), 0) / 255.
    shift_r40 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR40.png'), 0) / 255.

    levels = 5
    k_size = 13
    k_type = 'gaussian'
    sigma = 15
    interpolation = cv2.INTER_CUBIC
    border_mode = cv2.BORDER_REFLECT101

    u10, v10 = ps4.hierarchical_lk(shift_0, shift_r10, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    gaussian_sigma = 10
    gaussian_ksize = (15, 15)
    u10 = cv2.GaussianBlur(u10, gaussian_ksize, gaussian_sigma)
    v10 = cv2.GaussianBlur(v10, gaussian_ksize, gaussian_sigma)

    u_v = quiver(u10, v10, scale=1, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-a-1.png"), u_v)


    levels = 5
    k_size = 15
    k_type = 'gaussian'
    sigma = 3
    interpolation = cv2.INTER_CUBIC
    border_mode = cv2.BORDER_REFLECT101
    u20, v20 = ps4.hierarchical_lk(shift_0, shift_r20, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    gaussian_sigma = 20
    gaussian_ksize = (25, 25)
    u20 = cv2.GaussianBlur(u20, gaussian_ksize, gaussian_sigma)
    v20 = cv2.GaussianBlur(v20, gaussian_ksize, gaussian_sigma)

    u_v = quiver(u20, v20, scale=0.4, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-a-2.png"), u_v)

    levels = 5
    k_size = 67
    k_type = 'uniform'
    sigma = 70

    u40, v40 = ps4.hierarchical_lk(shift_0, shift_r40, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    u_v = quiver(u40, v40, scale=1, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-a-3.png"), u_v)


def part_4b():
    urban_img_01 = cv2.imread(
        os.path.join(input_dir, 'Urban2', 'urban01.png'), 0) / 255.
    urban_img_02 = cv2.imread(
        os.path.join(input_dir, 'Urban2', 'urban02.png'), 0) / 255.

    levels = 6
    k_size = 9
    k_type = "gaussian"
    sigma = 30
    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values

    u, v = ps4.hierarchical_lk(urban_img_01, urban_img_02, levels, k_size,
                               k_type, sigma, interpolation, border_mode)

    u_v = quiver(u, v, scale=0.2, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-b-1.png"), u_v)

    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values
    urban_img_02_warped = ps4.warp(urban_img_02, u, v, interpolation,
                                   border_mode)

    diff_img = urban_img_01 - urban_img_02_warped
    cv2.imwrite(os.path.join(output_dir, "ps4-4-b-2.png"),
                ps4.normalize_and_scale(diff_img))


def part_5a():
    """Frame interpolation

    Follow the instructions in the problem set instructions.

    Place all your work in this file and this section.
    """

    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq', 'ShiftR10.png'), 0) / 255.

    levels = 5
    k_size = 11
    k_type = 'gaussian'
    sigma = 15
    interpolation = cv2.INTER_CUBIC
    border_mode = cv2.BORDER_REFLECT101

    u, v = ps4.hierarchical_lk(shift_0, shift_r10, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    u_v = quiver(u, v, scale=1, stride=10)
    cv2.imwrite(os.path.join(output_dir, "quiver.png"), u_v)

    I00 = shift_0
    I02 = ps4.warp(shift_r10, 0.8 * u, 0.8 * v, interpolation, border_mode)
    I04 = ps4.warp(shift_r10, 0.6 * u, 0.6 * v, interpolation, border_mode)
    I06 = ps4.warp(shift_r10, 0.4 * u, 0.4 * v, interpolation, border_mode)
    I08 = ps4.warp(shift_r10, 0.2 * u, 0.2 * v, interpolation, border_mode)
    I10 = shift_r10

    cv2.imwrite(os.path.join(output_dir, "I00.png"), ps4.normalize_and_scale(I00))
    cv2.imwrite(os.path.join(output_dir, "I02.png"), ps4.normalize_and_scale(I02))
    cv2.imwrite(os.path.join(output_dir, "I04.png"), ps4.normalize_and_scale(I04))
    cv2.imwrite(os.path.join(output_dir, "I06.png"), ps4.normalize_and_scale(I06))
    cv2.imwrite(os.path.join(output_dir, "I08.png"), ps4.normalize_and_scale(I08))
    cv2.imwrite(os.path.join(output_dir, "I10.png"), ps4.normalize_and_scale(I10))

    # TODO: Create image collage for presentation


def part_5b():
    """Frame interpolation

    Follow the instructions in the problem set instructions.

    Place all your work in this file and this section.
    """

    mc01 = cv2.imread(os.path.join(input_dir, 'MiniCooper', 'mc01.png'), 0) / 255.
    mc02 = cv2.imread(os.path.join(input_dir, 'MiniCooper', 'mc02.png'), 0) / 255.
    mc03 = cv2.imread(os.path.join(input_dir, 'MiniCooper', 'mc03.png'), 0) / 255.
    shape = mc01.shape

    levels = 12
    k_size = 37
    k_type = 'gaussian'
    sigma = 8
    interpolation = cv2.INTER_CUBIC
    border_mode = cv2.BORDER_REFLECT101

    blur_mc01 = np.copy(mc01)
    blur_mc02 = np.copy(mc02)

    u, v = ps4.hierarchical_lk(blur_mc01, blur_mc02, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    gaussian_sigma = 5
    gaussian_ksize = (25, 25)
    u = cv2.GaussianBlur(u, gaussian_ksize, gaussian_sigma)
    v = cv2.GaussianBlur(v, gaussian_ksize, gaussian_sigma)

    u_v = quiver(u, v, scale=2, stride=10)
    cv2.imwrite(os.path.join(output_dir, "quiver1.png"), u_v)

    I10 = mc01
    I20 = mc02
    I30 = mc03

    I12 = ps4.warp(mc01, -0.4 * u, -0.4 * v, interpolation, border_mode)
    I14 = ps4.warp(mc01, -0.7 * u, -0.7 * v, interpolation, border_mode)
    I16 = ps4.warp(mc01, -1.0 * u, -1.0 * v, interpolation, border_mode)
    I18 = ps4.warp(mc01, -1.3 * u, -1.3 * v, interpolation, border_mode)
    # I12 = ps4.warp(mc02, 0.8 * u, 0.8 * v, interpolation, border_mode)
    # I14 = ps4.warp(mc02, 0.6 * u, 0.6 * v, interpolation, border_mode)
    # I16 = ps4.warp(mc02, 0.4 * u, 0.4 * v, interpolation, border_mode)
    # I18 = ps4.warp(mc02, 0.2 * u, 0.2 * v, interpolation, border_mode)

    res1 = np.concatenate([I10, I12, I14], axis=1)
    res2 = np.concatenate([I16, I18, I20], axis=1)
    res3 = np.concatenate([res1, res2])
    cv2.imwrite(os.path.join(output_dir, "ps4-5-b-1.png"), ps4.normalize_and_scale(res3))


    levels = 10
    k_size = 31
    k_type = 'uniform'
    sigma = 12
    interpolation = cv2.INTER_CUBIC
    border_mode = cv2.BORDER_REFLECT101
    u, v = ps4.hierarchical_lk(mc02, mc03, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    gaussian_sigma = 5
    gaussian_ksize = (25, 25)
    u = cv2.GaussianBlur(u, gaussian_ksize, gaussian_sigma)
    v = cv2.GaussianBlur(v, gaussian_ksize, gaussian_sigma)

    u_v = quiver(u, v, scale=2, stride=10)
    cv2.imwrite(os.path.join(output_dir, "quiver2.png"), u_v)

    I22 = ps4.warp(mc02, -0.4 * u, -0.4 * v, interpolation, border_mode)
    I24 = ps4.warp(mc02, -0.7 * u, -0.7 * v, interpolation, border_mode)
    I26 = ps4.warp(mc02, -1.0 * u, -1.0 * v, interpolation, border_mode)
    I28 = ps4.warp(mc02, -1.4 * u, -1.4 * v, interpolation, border_mode)
    # I22 = ps4.warp(mc03, 0.8 * u, 0.8 * v, interpolation, border_mode)
    # I24 = ps4.warp(mc03, 0.6 * u, 0.6 * v, interpolation, border_mode)
    # I26 = ps4.warp(mc03, 0.4 * u, 0.4 * v, interpolation, border_mode)
    # I28 = ps4.warp(mc03, 0.2 * u, 0.2 * v, interpolation, border_mode)

    res1 = np.concatenate([I20, I22, I24], axis=1)
    res2 = np.concatenate([I26, I28, I30], axis=1)
    res3 = np.concatenate([res1, res2])
    cv2.imwrite(os.path.join(output_dir, "ps4-5-b-2.png"), ps4.normalize_and_scale(res3))


    cv2.imwrite(os.path.join(output_dir, "I10.png"), ps4.normalize_and_scale(I10))
    cv2.imwrite(os.path.join(output_dir, "I12.png"), ps4.normalize_and_scale(I12))
    cv2.imwrite(os.path.join(output_dir, "I14.png"), ps4.normalize_and_scale(I14))
    cv2.imwrite(os.path.join(output_dir, "I16.png"), ps4.normalize_and_scale(I16))
    cv2.imwrite(os.path.join(output_dir, "I18.png"), ps4.normalize_and_scale(I18))
    cv2.imwrite(os.path.join(output_dir, "I20.png"), ps4.normalize_and_scale(I20))
    cv2.imwrite(os.path.join(output_dir, "I22.png"), ps4.normalize_and_scale(I22))
    cv2.imwrite(os.path.join(output_dir, "I24.png"), ps4.normalize_and_scale(I24))
    cv2.imwrite(os.path.join(output_dir, "I26.png"), ps4.normalize_and_scale(I26))
    cv2.imwrite(os.path.join(output_dir, "I28.png"), ps4.normalize_and_scale(I28))
    cv2.imwrite(os.path.join(output_dir, "I30.png"), ps4.normalize_and_scale(I30))


def part_6():
    """Challenge Problem

    Follow the instructions in the problem set instructions.

    Place all your work in this file and this section.
    """

    raise NotImplementedError


if __name__ == '__main__':
    # part_1a()
    # part_1b()
    # part_2()
    # part_3a_1()
    # part_3a_2()
    # part_4a()
    # part_4b()
    # part_5a()
    part_5b()
    # part_6()
