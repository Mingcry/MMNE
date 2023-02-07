import os
import re
import csv


def inverse(d):
    res = {}
    for item in d:
        res[d[item]] = item
    return res


info = {
        '电影名': 0, '电影网址': 1, '导演': 2, '编剧': 3, '主演': 4,
        '评分': 5, '评分人数': 6, '评分额外信息': 7,
        '类型': 8, '制片国家/地区': 9, '语言': 10, '上映时间': 11, '时长': 12,
        '剧情简介': 13, '获奖情况': 14, '热门评论': 15,
        '海报链接': 16, '海报保存路径': 17, '剧照链接': 18, '剧照保存路径': 19, '视频链接': 20, '视频保存路径': 21
    }
ids = inverse(info)

wjj_list = ['data', 'data1', 'data2', 'data3']
file_list = os.listdir('./' + wjj_list[0] + '/movie_info')
for index, file in enumerate(file_list):
    path = './' + wjj_list[0] + '/movie_info/' + file
    # print(path)

    data = []
    with open(path, 'r', encoding='utf-8') as f:
        csv_read = csv.reader(f)
        for i, row in enumerate(csv_read):
            if i:
                data.append(row)
    num_movie = len(data)
    # print('num:', num_movie)

    director_index = {}
    # root
    director = data[0][info['导演']]
    # print(director)

    k = 0
    for i in range(num_movie):
        movie = data[i]
        for j, item in enumerate(movie):
            if item == 'INF':
                movie[j] = '暂无'
            if j < 16:
                movie[j] = re.sub(' ', '', movie[j].strip('\n'))

        valid = True
        information = {}
        film = []

        # level1
        name = movie[info['电影名']]
        # print(name)
        film.append(name)

        # level2 text-1
        introduction = 'None'
        if movie[info['剧情简介']] != '暂无':
            introduction = '剧情简介是' + movie[info['剧情简介']]
        else:
            valid = False
        # print(introduction)
        information[len(information)] = introduction

        # level2 text-2
        base = []
        actor = '主演是'
        if movie[info['主演']] != '暂无':
            actor += ','.join(eval(movie[info['主演']]))
        else:
            actor += '暂无'
        base.append(actor)
        writer = '编剧是' + re.sub('/', '、', movie[info['编剧']])
        base.append(writer)
        for i in range(8, 13):
            base.append(ids[i] + '是' + re.sub('/', '、', movie[i]))
        base_info = '。'.join(base) + '。'
        # print(base_info)
        information[len(information)] = base_info

        # level2 text-3
        commends = ''.join(eval(movie[info['热门评论']]))
        if not commends:
            commends = 'None'
        # print(commends)
        information[len(information)] = commends

        # level2 text-4
        addition = ''
        if movie[info['评分额外信息']] != '暂无':
            addition += movie[info['评分额外信息']] + '。'
        if movie[info['获奖情况']] != '暂无':
            addition += '。'.join(eval(movie[info['获奖情况']])) + '。'
        if not addition:
            addition = 'None'
        # print(addition)
        information[len(information)] = addition

        # level2 image
        image_path = movie[info['海报保存路径']]
        image = os.listdir(image_path)
        if image:
            image = str([image_path + '/' + item for item in image])
        else:
            image = 'None'
        # print(image)
        information[len(information)] = image

        # level2 video
        video_path = movie[info['视频保存路径']]
        video = os.listdir(video_path)
        if video:
            video = str([video_path + '/' + item for item in video])
        else:
            video = 'None'
        # print(video)
        information[len(information)] = video

        film.append(information)

        if valid:
            dir_name = './new_data'
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            save_path = dir_name + '/' + str(index) + '.txt'
            with open(save_path, 'a+', encoding='utf-8') as f:
                f.write(str(k) + '\t' + str(film) + '\n')
                k += 1

    director_index[index] = (director, k)
    with open('./director_index.txt', 'a+') as f:
        f.write(str(director_index) + '\n')
