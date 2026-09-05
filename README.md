# Paulo — website & web build

Astro site published on GitHub Pages at https://kuragestudios.github.io/paulo/

- `/` landing page (features, screenshots, download links)
- `/play/` the game, full window
- `/game/` the raw Unity WebGL build (copied from the Unity project by `Deploy/github-pages/publish-web.sh`)

```sh
npm install
npm run dev      # http://localhost:4321/paulo/
npm run build    # dist/
```

Deploy: push to `main`; `.github/workflows/deploy.yml` builds and publishes to Pages
(Settings > Pages > Source: GitHub Actions).

Sprites in `public/images/sprites/` are exported from the Unity project by `scripts/sprites.py`
(needs Pillow: `pip install pillow`).
