import os
import sys
import subprocess

def run_and_compare(folder_path, run_command):
    """テストケースを実行し、出力を比較"""
    testcases = len([f for f in os.listdir(folder_path) if f.startswith('input')])
    for i in range(testcases):
        with open(f'{folder_path}/input_{i}.txt', 'r') as f:
            input_data = f.read()
        with open(f'{folder_path}/output_{i}.txt', 'r') as f:
            expected_output = f.read()
        process = subprocess.run(run_command, input=input_data.encode(), stdout=subprocess.PIPE)
        if process.stdout.decode() != expected_output:
            print(f'Failed on test case {i}')
            print('Input:')
            print(input_data)
            print('Expected output:')
            print(expected_output)
            print('Your output:')
            print(process.stdout.decode())
        else:
            print(f'Passed on test case {i}')

def build_and_run(file_or_folder_path):
    """フォルダ内のファイルをコンパイルし、テストケースを実行"""
    # 与えられたパスからフォルダ名とファイル名を取得
    folder_path = os.path.dirname(file_or_folder_path)
    file_name = os.path.basename(file_or_folder_path)
    # ファイル名が指定されていない場合、フォルダ名をファイル名とする
    if not file_name:
        file_name = folder_path.split('/')[-1]

    def a(file):
        """相対パスを絶対パスに変換する"""
        return os.path.join(folder_path, file)

    # フォルダ内のファイルを取得
    for file in os.listdir(folder_path):
        if file.startswith(f'{file_name}.'):
            if file.endswith('.cpp') or file.endswith('.cc'):
                main_file = a('main')
                # コンパイル
                subprocess.run(['g++', '-o', main_file, a(file)])
                run_command = [main_file]
            elif file.endswith('.py'):
                run_command = ['python', a(file)]
            elif file.endswith('.rs'):
                main_file = a('main')
                # コンパイル
                subprocess.run(['rustc', '-o', main_file, a(file)])
                run_command = [main_file]
            else:
                continue
            # テストケースを実行
            run_and_compare(folder_path, run_command)

if __name__ == "__main__":
    # 引数をもとにパスを取得
    file_or_folder_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    build_and_run(file_or_folder_path)
