"""
プログラミングコンテスト毎に必要なクラスの共通処理をまとめたクラス
"""

import os

class CompProgTemplate():
    def init(self):
        self.key_dict = None
        self.code_template_location = None

    def create_files(self, description, testcase, folder_name, file_name, template_type):
        """フォルダとファイルを作成"""
        os.makedirs(folder_name, exist_ok=True)
        # ソースコードのテンプレートファイルを読み込み
        with open(f'{self.code_template_location}/{template_type}', 'r') as f:
            template = f.read()
            # テンプレート内の{}で囲まれた部分がkey_dictに含まれている場合、それに対応する値で置換
            for key, val in self.key_dict.items():
                template = template.replace(f'{{{key}}}', str(description[val]))
            # ファイルを作成し、テンプレートを書き込む
            with open(f'{folder_name}/{file_name}.{template_type}', 'w') as f:
                f.write(template)
            # テストケースを作成
            for i, test in enumerate(testcase):
                with open(f'{folder_name}/input_{i+1}.txt', 'w') as f:
                    f.write(test['in'])
                with open(f'{folder_name}/output_{i+1}.txt', 'w') as f:
                    f.write(test['out'])
