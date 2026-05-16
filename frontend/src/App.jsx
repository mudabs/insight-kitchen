import {
  SignedIn,
  SignedOut,
  SignInButton,
  UserButton,
} from '@clerk/clerk-react'
import { useAuth } from "@clerk/clerk-react"

function App() {
  const { getToken } = useAuth()

  return (
    <div style={{ padding: '2rem' }}>

      <h1>Insight Kitchen</h1>

      <SignedOut>
        <SignInButton />
      </SignedOut>

      <SignedIn>
        <UserButton />

        <h2>You are signed in.</h2>

        {/* <button
          onClick={async () => {
            const token = await getToken({
              template: "backend"
            })

            console.log(token)
          }}
        >
          Print Token
        </button> */}

        <button
          onClick={async () => {

            try {

              const token = await getToken({
                template: "backend",
                skipCache: true
              })

              console.log("TOKEN:")
              console.log(token)

            } catch (err) {

              console.error("TOKEN ERROR:")
              console.error(err)

            }

          }}
        >
          Print Token
        </button>

      </SignedIn>

    </div>
  )
}

export default App