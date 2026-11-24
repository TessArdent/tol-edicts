import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://example.github.io",   // replaced with the real Pages URL in TO-5
  base: "/tol-edicts",
  trailingSlash: "always",
  output: "static",
  build: { format: "directory" },
});
