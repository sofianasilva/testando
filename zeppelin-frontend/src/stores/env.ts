interface EnvConfig {
  API_BASE_URL: string
  CLIENT_ID: string
  CLIENT_SECRET: string
  ZEPPELIN_API_TOKEN: string
}

export const env: EnvConfig = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL as string,
  CLIENT_ID: import.meta.env.VITE_CLIENT_ID as string,
  CLIENT_SECRET: import.meta.env.VITE_CLIENT_SECRET as string,
  ZEPPELIN_API_TOKEN: import.meta.env.VITE_ZEPPELIN_API_TOKEN as string
}