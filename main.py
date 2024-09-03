import os
import getpass


def run_certbot(domain, email):
    letsencrypt_dir = os.path.join(os.getcwd(), "letsencrypt")
    lib_dir = os.path.join(os.getcwd(), "lib")

    os.makedirs(letsencrypt_dir, exist_ok=True)
    os.makedirs(lib_dir, exist_ok=True)

    print(f"Generating certificate for domain: {domain}")

    cmd = (
        f"docker run -it --rm --name certbot "
        f"-v {letsencrypt_dir}:/etc/letsencrypt "
        f"-v {lib_dir}:/var/lib/letsencrypt "
        "certbot/certbot certonly "
        "--manual "
        "--preferred-challenges dns "
        f"--domain {domain} "
        f"--email {email} "
        "--agree-tos "
        "--rsa-key-size 2048"
    )

    os.system(cmd)


def convert_to_pfx(domain, password):
    letsencrypt_dir = os.path.join(os.getcwd(), "letsencrypt")
    domain_dir = os.path.join(letsencrypt_dir, "live", domain)
    cert_path = os.path.join(domain_dir, "fullchain.pem")
    key_path = os.path.join(domain_dir, "privkey.pem")
    pfx_path = f"{domain}.pfx"

    print(f"Converting certificate to PFX format: {pfx_path}")

    os.system(f"openssl pkcs12 -export -out {pfx_path} -inkey {key_path} -in {cert_path} -password pass:{password}")

    print(f"PFX file created at: {pfx_path}")
    return pfx_path


def main():
    domain = input("Enter your domain: ")
    email = input("Enter your email address: ")
    password = getpass.getpass("Enter a password for the PFX file: ")

    run_certbot(domain, email)
    pfx_file = convert_to_pfx(domain, password)

    print(f"Certificate generated and saved to {pfx_file}")


if __name__ == "__main__":
    main()