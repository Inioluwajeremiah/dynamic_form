import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import FormProvider from '../store/provider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'DynamicForm App',
  description: 'Simple Dynamic form PWA',
  manifest: '/manifest.json',
  icons: {apple:'/icon.png'},
  themeColor: '#fff'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return ( <>
    <html lang="en">
        <body className={inter.className}>
          <FormProvider>
          {children}
          </FormProvider>
          
        </body>
    </html>
  </>
   
  )
}
