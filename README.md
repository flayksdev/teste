# Site pessoal — Flayks Oliveira

Software Engineer • Founder • AI & Cybersecurity

## Estado atual

| Parte | Estado |
|---|---|
| `frontend/` | Site estático (HTML, CSS e JavaScript, sem dependências). Verificado em Chromium headless: sem erros de console, sem imagens quebradas, sem rolagem horizontal em 390 px e 1366 px, tema claro e escuro. |
| `backend/` | Rascunho FastAPI anterior (config, modelos, segurança, seed). **Ainda não tem `main.py`, rotas, migrações nem testes, e nunca foi executado.** O frontend ainda não depende dele. |

## Ver o site localmente

```bash
cd frontend
python3 -m http.server 8000
# abra http://localhost:8000
```

Também pode ser publicado como está (GitHub Pages, Netlify, Cloudflare Pages ou qualquer servidor estático), apontando para a pasta `frontend/`.

## Conteúdo

Todo o texto vem de informações fornecidas pelo próprio Flayks. Nada de clientes, métricas, empregos ou diplomas foi acrescentado. Projetos em desenvolvimento aparecem como tal. O telefone não é exibido no site.

## Segurança do frontend

- CSP restritiva via `<meta>` (`default-src 'self'`, sem scripts ou estilos inline, sem recursos externos).
- Sem fontes, scripts ou trackers de terceiros.
- Links externos com `rel="noopener noreferrer"`.
- Ao publicar, configure também no servidor os cabeçalhos `Content-Security-Policy` (com `frame-ancestors 'none'`), `X-Content-Type-Options: nosniff` e HSTS, que um `<meta>` não consegue definir.

## Próximos passos

1. Completar o backend (rotas, autenticação, painel administrativo, migrações, testes) e só então ligar o frontend à API.
2. Migrar o frontend para Next.js + TypeScript quando houver acesso ao registro npm no ambiente de desenvolvimento.
3. Definir o domínio e trocar `og:image` por uma URL absoluta.
