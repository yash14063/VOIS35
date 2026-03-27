import twilio from "twilio";

const client = twilio(process.env.TWILIO_SID, process.env.TWILIO_AUTH);
const serviceSid = process.env.TWILIO_SERVICE;

const allowedNumber = "+919767127989";

export default async function handler(req, res) {

    if (req.method !== "POST") {
        return res.status(405).json({ error: "Method not allowed" });
    }

    const { phone } = req.body;

    if (phone !== allowedNumber) {
        return res.status(403).json({ error: "Unauthorized" });
    }

    try {
        await client.verify.v2.services(serviceSid)
            .verifications
            .create({ to: phone, channel: "sms" });

        res.status(200).json({ success: true });

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
}
