import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Emojis were completely garbled, let's just do regex replacements based on the text next to them
    content = re.sub(r'<h3 class="text-sm font-bold text-red-500 uppercase tracking-widest mb-3 border-l-2 border-red-500 pl-2">.*BUGS_DETECTED</h3>', 
                     '<h3 class="text-sm font-bold text-red-500 uppercase tracking-widest mb-3 border-l-2 border-red-500 pl-2">🐛 BUGS_DETECTED</h3>', content)
                     
    content = re.sub(r'<h3 class="text-sm font-bold text-yellow-500 uppercase tracking-widest mb-3 border-l-2 border-yellow-500 pl-2">.*STYLE_VIOLATIONS</h3>', 
                     '<h3 class="text-sm font-bold text-yellow-500 uppercase tracking-widest mb-3 border-l-2 border-yellow-500 pl-2">🎨 STYLE_VIOLATIONS</h3>', content)

    content = re.sub(r'<h3 class="text-sm font-bold text-blue-400 uppercase tracking-widest mb-3 border-l-2 border-blue-400 pl-2">.*OPTIMIZATION_VECTORS</h3>', 
                     '<h3 class="text-sm font-bold text-blue-400 uppercase tracking-widest mb-3 border-l-2 border-blue-400 pl-2">💡 OPTIMIZATION_VECTORS</h3>', content)

    content = re.sub(r'<h3 class="text-sm font-bold text-base-text uppercase tracking-widest mb-3 border-l-2 border-base-500 pl-2">.*ARCHITECTURE_SUMMARY</h3>', 
                     '<h3 class="text-sm font-bold text-base-text uppercase tracking-widest mb-3 border-l-2 border-base-500 pl-2">📖 ARCHITECTURE_SUMMARY</h3>', content)

    content = re.sub(r'None identified .*</li>', 'None identified ✅</li>', content)

    # Add credentials to fetch!
    content = content.replace("fetch('/api/review', {", "fetch('/api/review', {\n                credentials: 'same-origin',")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('app/templates/index.html')
fix_file('app/templates/history.html')
