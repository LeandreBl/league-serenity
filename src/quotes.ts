import jsonQuotes from './locales/quotes.json' assert { type: 'json' }

interface QuoteSound {
  languages: Record<string, string>
  soundpaths: Record<string, string>
}

export default jsonQuotes as QuoteSound[]
