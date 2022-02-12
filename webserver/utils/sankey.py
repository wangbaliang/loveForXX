
# -*- coding: utf-8 -*-

__author__ = 'wgs@test'


import os
import json
import copy

from pyecharts.charts import Page, Sankey
from pyecharts import options as opts
from pyecharts.globals import ThemeType

def gen_html_path(task_id):
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(root_path, 'templates', '%s_result.html' % str(task_id))
    return html_path


def gen_class_name(year, u_class, topic):
    return year + '类别' + u_class + '[%s]' % topic


def gen_none_name(year):
    return year + "后新增"



def create_sankey(task_id, file_path):

    if not os.path.exists(file_path):
        print("not exist file_path")
        return

    with open(file_path) as fp:
        evo = json.load(fp)

    nodes = []
    links = []
    links_more = []
    node_item = {}




    evo_keys = sorted(evo)

    for i in range(len(evo_keys)):

        year = evo_keys[i]

        if year != evo_keys[-1]:
            nodes.append({'name': gen_none_name(year), 'depth': i, 'symbolSize': 10})
        year_class_info_dict = evo[year]

        for u_class, year_class_info in year_class_info_dict.items():
            name = gen_class_name(year, u_class, year_class_info['keyword_list'][0])
            node_item[name] = {
                "name": name,
                "doc_list": year_class_info["doc_list"],
            }
            nodes.append({'name': name, 'depth': i, 'symbolSize': 20})


    for i in range(len(evo_keys)):
        if i == 0:
            continue
        year = evo_keys[i]
        pre_year = evo_keys[i - 1]

        year_class_dict = evo[year]
        pre_year_class_dict = evo[pre_year]

        # 前一年出现的ids
        dd = []
        # 前一年后新增的ids
        dd1 = []

        year_class_dict_sorted = sorted(year_class_dict)
        print(222222, year, year_class_dict_sorted)
        for u_class in year_class_dict_sorted:
            year_class = year_class_dict[u_class]
            none_year_class = copy.deepcopy(year_class['doc_list'])

            pre_year_class_dict_sorted = sorted(pre_year_class_dict)
            print(3333333, pre_year, pre_year_class_dict_sorted)

            for pre_class in pre_year_class_dict_sorted:
                pre_year_class = pre_year_class_dict[pre_class]

                same_doc_list = []
                for i in year_class['doc_list']:
                    if i in pre_year_class['doc_list']:
                        same_doc_list.append(i)
                        none_year_class.remove(i)
                        dd.append(i)


                link_more = {
                    'source': gen_class_name(pre_year, pre_class, pre_year_class['keyword_list'][0]),
                    'target': gen_class_name(year, u_class, year_class['keyword_list'][0]),
                    'doc': same_doc_list,
                    'value': len(same_doc_list)
                }
                links_more.append(link_more)

            dd1 = dd1 + none_year_class
            #             print(1111111111, year, u_class, pre_year, pre_class, year_class['doc_list'], pre_year_class['doc_list'], same_doc_list)

            none_year_link = {
                'source': gen_none_name(pre_year),
                'target': gen_class_name(year, u_class, year_class['keyword_list'][0]),
                'doc': none_year_class,
                'value': len(none_year_class)
            }
            links_more.append(none_year_link)



    links = [{'source': i['source'], 'target': i['target'], 'value': i['value']} for i in links_more if i['value'] > 0]

    c = (
            Sankey(init_opts=opts.InitOpts(width='800px', height='450px'))
            .add(
                "任务: %s" % task_id,
                nodes,
                links,
                linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source",type_="dotted"),
                label_opts=opts.LabelOpts(is_show=False),#(position="right",),
                focus_node_adjacency='allEdges',
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="主题演进桑基图"))
        )
    # 输出html可视化结果
    c.render(gen_html_path(task_id))


if __name__ == '__main__':
    import sys

    task_id = sys.argv[1]
    path = sys.argv[2]
    create_sankey(task_id, path)
