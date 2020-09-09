module.exports = {
  root: true,
  extends: [
    'eslint:recommended',
    'plugin:import/errors',
    'plugin:import/warnings',
    'plugin:prettier/recommended',
  ],
  parser: 'babel-eslint',
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    allowImportExportEverywhere: true,
    ecmaFeatures: {
      impliedStrict: true,
    },
  },
  env: {
    browser: true,
    node: true,
  },
  plugins: ['html'],
  settings: {
    'import/resolver': {
      node: {
        moduleDirectory: ['web_modules'],
      },
    },
  },
};
