import { exec } from "child_process";

function cleanupAndExit() {

    const name = process.env.PM2_PROCESS_NAME;

    exec(`pm2 delete ${name}`, (err, stdout) => {

        if (err) console.log("Failed to remove PM2 session:", err);

        console.log(`PM2 session ${name} deleted.`);

        process.exit(0);

    });

}

export default cleanupAndExit;