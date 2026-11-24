import { defineConfig } from "astro/config";

// In GitHub Actions these come from actions/configure-pages, so the site works
// under any account or repository name. Locally they default to /tol-edicts.
const origin = process.env.SITE_ORIGIN || "http://localhost:4321";
// An empty BASE_PATH (a username.github.io repository) means the site root.
const base = process.env.BASE_PATH === undefined ? "/tol-edicts" : process.env.BASE_PATH || "/";

export default defineConfig({
  site: origin,
  base,
  trailingSlash: "always",
  output: "static",
  build: { format: "directory" },
});
