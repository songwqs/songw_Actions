import os
import json
import requests

def get_image_paths(repo_owner, repo_name, path, github_token, base_path):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"Bearer {github_token}"}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    contents = response.json()

    image_paths = []

    for item in contents:
        if item["type"] == "file" and item["name"].lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
            full_path = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{path}/{item['name']}"
            image_paths.append(full_path)

    return image_paths

def main():
    repo_owner = "songwqs"
    repo_name = "cdnImg"
    base_path = "hacg"
    github_token = os.environ['GITHUB_TOKEN']

    # 打印工作目录和基本路径以进行调试
    print(f"工作目录: {os.environ['GITHUB_WORKSPACE']}")
    print(f"基本路径: {base_path}")

    # 使用 GitHub Actions 的工作目录作为基本路径
    work_dir = os.environ['GITHUB_WORKSPACE']
    base_path = os.path.join(work_dir, base_path)

    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"已创建文件夹: {base_path}")

    all_image_paths = []

    for subdir in os.listdir(base_path):
        subdir_path = os.path.join(base_path, subdir)
        if os.path.isdir(subdir_path):
            subdir_image_paths = get_image_paths(repo_owner, repo_name, f"{base_path}/{subdir}", github_token, base_path)
            all_image_paths.extend(subdir_image_paths)

    with open('image_paths.json', 'w') as json_file:
        json.dump(all_image_paths, json_file, indent=2)

    # 读取并打印输出 image_paths.json 的内容
    with open('image_paths.json', 'r') as json_file:
        content = json_file.read()
        print(content)

if __name__ == "__main__":
    main()
