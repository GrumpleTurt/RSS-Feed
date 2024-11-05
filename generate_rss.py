import datetime
import hashlib
import os
import xml.etree.ElementTree as ET

# Path to the input file with passages
input_file = "Enchiridion.txt"
output_file = "daily_feed.xml"  # The generated RSS feed file

# Function to parse passages from the text file
def get_passages():
    with open(input_file, "r") as f:
        passages = f.read().split("\n\n")  # Assumes passages are separated by double newlines
    return [p.strip() for p in passages if p.strip()]

# Function to generate RSS XML structure
def create_rss_feed(passages):
    # Create RSS root structure
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "The Enchiridion Daily Feed"
    ET.SubElement(channel, "link").text = "https://github.com/GrumpleTurt/RSS-Feed"
    ET.SubElement(channel, "description").text = "Daily passages from The Enchiridion."

    # Calculate which passage to show today based on the date
    today = datetime.datetime.utcnow().date()
    index = today.toordinal() % len(passages)  # Cycle through passages
    passage = passages[index]

    # Create an RSS item for the passage
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"Passage {index + 1}"
    ET.SubElement(item, "description").text = passage
    ET.SubElement(item, "pubDate").text = today.strftime("%a, %d %b %Y 00:00:00 +0000")
    ET.SubElement(item, "guid").text = hashlib.md5(passage.encode()).hexdigest()  # Unique ID for the item

    # Write to XML
    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Main execution
if __name__ == "__main__":
    passages = get_passages()
    create_rss_feed(passages)
