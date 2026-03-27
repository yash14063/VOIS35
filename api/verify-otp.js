import twilio from "twilio";

const client = twilio(process.env.TWILIO_SID, process.env.TWILIO_AUTH);
const serviceSid = process.env.TWILIO_SERVICE;

export default async function handler(req, res) {

    if (req.method !== "POST") {
        return res.status(405).json({ error: "Method not allowed" });
    }

    const { phone, code } = req.body;

    try {
        const check = await client.verify.v2.services(serviceSid)
            .verificationChecks
            .create({ to: phone, code });

        if (check.status === "approved") {
            res.status(200).json({ success: true });
        } else {
            res.status(200).json({ success: false });
        }

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
}
