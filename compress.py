from PIL import Image
import os
import shutil

def smart_compress(input_path, target_kb=150, max_dim=1920, min_quality=10):
    """
    智能压缩大图片到指定大小（KB），直接覆盖原图
    """
    # 先备份原图
    # backup_path = input_path + ".bak"
    # if not os.path.exists(backup_path):
    #     shutil.copy2(input_path, backup_path)

    try:
        img = Image.open(input_path)
    except Exception as e:
        print(f"❌ 跳过无法识别的文件: {input_path} ({e})")
        return

    img_format = img.format

    # 缩放图片
    img.thumbnail((max_dim, max_dim))

    # 如果是 PNG 且带透明通道，先转成白色背景的 RGB
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background

    # 初始质量
    quality = 85
    step = 5

    try:
        while True:
            img.save(input_path, format="JPEG", quality=quality, optimize=True)
            size_kb = os.path.getsize(input_path) / 1024
            if size_kb <= target_kb or quality <= min_quality:
                break
            quality -= step
    except Exception as e:
        print(f"❌ 压缩失败: {input_path} ({e})")
        return

    print(f"✅ 压缩完成: {input_path} ({os.path.getsize(input_path)/1024:.1f} KB, 质量: {quality})")

def batch_smart_compress(input_folder, target_kb=150, max_dim=1920):
    for file in os.listdir(input_folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_folder, file)
            smart_compress(input_path, target_kb, max_dim)

# 使用：直接压缩原目录里的图片
batch_smart_compress(
    # "themes/myhui/source/img/articleslist",
    # "themes/myhui/source/img/random",
    "themes/myhui/source/img/homepage",
    target_kb=150,
    max_dim=1920
)
