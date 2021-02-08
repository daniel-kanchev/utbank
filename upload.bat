git init -b main
git add .
git commit -m "Finished Script"
gh repo create utbank -y --public
git remote add origin https://github.com/daniel-kanchev/utbank.git
git push origin main