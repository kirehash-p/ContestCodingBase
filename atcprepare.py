"""
AtCoderの問題を解くためのテンプレートを作成するスクリプト
引数には問題のIDとタイトル(省略可)を指定する
"""

import sys
import requests
from bs4 import BeautifulSoup
import os
import time
import json
import re

from src.scripts import prepare_template

# テンプレートの言語。src/code_templates/atcoderフォルダ内のファイル名と一致させる。
template_type = "rs"
# ファイルなどを生成するディレクトリ
target_dir = ""

class AtCoder(prepare_template.CompProgTemplate):
    def __init__(self):
        self.key_dict = {
            "問題ID": "problem_id",
            "問題名": "problem_name",
            "問題タイトル": "problem_title",
            "問題番号": "problem_index",
            "コンテストID": "contest_id",
            "コンテスト名": "contest_title",
            "コンテスト開始時刻": "contest_start_time",
            "コンテスト制限時間": "contest_duration_second",
            "レート対象": "contest_rate_change",
            "メモリ制限": "memory_limit",
            "実行時間制限": "time_limit",
        }
        self.code_template_location = 'src/code_templates/atcoder'

    def get_folder_name(self, description):
        """フォルダ名の生成"""
        return f'{description["contest_id"]}/{self.get_file_name(description)}'

    def get_file_name(self, description):
        """ファイル名の生成"""
        return description["problem_id"]

    def get_json_data(self, problem_id):
        """kenkoooo.comのAPIを使って問題の情報を取得"""
        contests = './src/json/contests.json'
        problems = './src/json/problems.json'
        # contest_problem = './src/json/contest_problem.json' # contest_problem ∈ problems であるため使用しない

        # ファイルが存在しない、または更新日時が1日以上前の場合はダウンロード
        if not os.path.exists(contests) or os.path.getmtime(contests) < time.time() - 86400:
            url = 'https://kenkoooo.com/atcoder/resources/contests.json'
            res = requests.get(url)
            with open(contests, 'w') as f:
                f.write(res.text)
        if not os.path.exists(problems) or os.path.getmtime(problems) < time.time() - 86400:
            url = 'https://kenkoooo.com/atcoder/resources/problems.json'
            res = requests.get(url)
            with open(problems, 'w') as f:
                f.write(res.text)
        # if not os.path.exists(contest_problem) or os.path.getmtime(contest_problem) < time.time() - 86400:
        #     url = 'https://kenkoooo.com/atcoder/resources/contest-problem.json'
        #     res = requests.get(url)
        #     with open(contest_problem, 'w') as f:
        #         f.write(res.text)

        description = {}

        # with open(contests, 'r') as contests_file, open(problems, 'r') as problems_file, open(contest_problem, 'r') as contest_problem_file:
        with open(contests, 'r') as contests_file, open(problems, 'r') as problems_file:
            contests_data = json.load(contests_file)
            problems_data = json.load(problems_file)
            # contest_problem_data = json.load(contest_problem_file)
            description = {}
            description['problem_id'] = problem_id
            for problem in problems_data:
                if problem['id'] == problem_id:
                    description.update({
                        "contest_id": problem['contest_id'],
                        "problem_index": problem['problem_index'],
                        "problem_name": problem['name'],
                        "problem_title": problem['title']
                    })
                    break
            for contest in contests_data:
                if contest['id'] == description['contest_id']:
                    description.update({
                        "contest_start_epoch_second": contest['start_epoch_second'],
                        "contest_duration_second": contest['duration_second'],
                        "contest_title": contest['title'],
                        "contest_rate_change": contest['rate_change']
                    })
                    break
            # for contest_problem in contest_problem_data:
            #     if contest_problem['contest_id'] == description['contest_id'] and contest_problem['problem_id'] == id:
            #         description.update({
            #         })
            #         break

        return description

    def get_site_data(self, url):
        """AtCoderの問題ページから問題の情報を取得"""
        res_text = requests.get(url).text
        soup = BeautifulSoup(res_text, 'html.parser')
        description = {}
        description['problem_title'] = soup.find('title').text
        description['problem_name'] = description['problem_title'].split(' - ')[1]
        description['problem_index'] = description['problem_title'].split(' - ')[0]
        description['contest_title'] = soup.find('a', class_='contest-title').text
        mem_time_limit = soup.find(id='task-statement').find_previous_sibling('p').get_text().replace('\t', '').replace('\n', '').split(' / ')
        description['time_limit'] = mem_time_limit[0].split(': ')[1]
        description['memory_limit'] = mem_time_limit[1].split(': ')[1]
        description['contest_start_time'] = re.search(r'var\s+startTime\s*=\s*moment\("([^"]+)"\);', res_text).group(1)
        description['contest_end_time'] = re.search(r'var\s+endTime\s*=\s*moment\("([^"]+)"\);', res_text).group(1)

        tmp_test = []
        ja_page = soup.find(id='task-statement').find(class_='lang-ja').find_all(class_="part", recursive=False)
        for i in ja_page:
            if i.find('pre'):
                tmp_test.append(i.find('pre').text)
        testcase = []
        for i in range(0, len(tmp_test), 2):
            testcase.append({
                'in': tmp_test[i],
                'out': tmp_test[i+1]
            })

        return description, testcase

    
    def get_data(self, arg):
        """AtCoderの問題ページから問題の情報を取得"""
        # argがatcoderのurlの場合
        atcoder_url = re.match(r"https://atcoder\.jp/contests/([^/]+)/tasks/([^/]+)", arg)
        if atcoder_url:
            contest_id = atcoder_url.group(1)
            problem_id = atcoder_url.group(2)
            json_description = self.get_json_data(problem_id)
            json_description.update({
                "contest_id": contest_id,
            })
        else:
            json_description = self.get_json_data(arg)
            if not json_description:
                raise Exception('Problem not found. Try inputting the valid URL')
        url = arg if atcoder_url else f"https://atcoder.jp/contests/{json_description['contest_id']}/tasks/{json_description['problem_index']}"
        description, testcase = self.get_site_data(url)
        description.update(json_description)

        return description, testcase

if __name__ == '__main__':
    contest = AtCoder()
    arg = sys.argv[1]
    description, testcase = contest.get_data(arg)
    folder_name = os.path.join(target_dir, contest.get_folder_name(description))
    file_name = contest.get_file_name(description)
    contest.create_files(description, testcase, folder_name, file_name, template_type)