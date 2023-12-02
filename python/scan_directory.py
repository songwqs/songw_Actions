import os
import json
import requests

def get_github_contents(repo_owner, repo_name, path):
    github_token = os.environ.get('GITHUB_TOKEN')
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}'
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return None

def extract_download_links(contents):
    download_links = []

    for item in contents:
        if item['type'] == 'dir':
            # 递归遍历子目录
            sub_contents = get_github_contents(repo_owner, repo_name, item['path'])
            download_links.extend(extract_download_links(sub_contents))
        elif 'download_url' in item:
            download_links.append(item['download_url'])

    return download_links

def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

if __name__ == '__main__':
    # 替换为你的 GitHub 仓库信息和目标目录
    repo_owner = 'songwqs'
    repo_name = 'cdnImg'
    path = 'hacg'
    
    # 替换为你想要保存的 JSON 文件路径
    output_file = 'image_paths.json'

    contents = get_github_contents(repo_owner, repo_name, path)

    if contents:
        download_links = extract_download_links(contents)
        save_to_json(download_links, output_file)
