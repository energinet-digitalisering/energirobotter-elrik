from cv_bridge import CvBridge
from ultralytics import YOLO

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CompressedImage
from vision_msgs.msg import BoundingBox2D, Pose2D, Point2D


class FaceDetectionNode(Node):

    def __init__(self):
        super().__init__("face_detection_node")

        # Parameters
        self.declare_parameter("use_compressed", False)
        self.use_compressed = (
            self.get_parameter("use_compressed").get_parameter_value().bool_value
        )

        # Subscriptions
        if self.use_compressed:
            self.subscription = self.create_subscription(
                CompressedImage, "/camera", self.camera_callback, 10
            )
        else:
            self.subscription = self.create_subscription(
                Image, "/camera", self.camera_callback, 10
            )

        # Publishers
        self.publisher_annotation = self.create_publisher(Image, "/camera_annotated", 1)

        self.publisher_bounding_box = self.create_publisher(
            BoundingBox2D, "/face_bounding_box", 1
        )

        # Node variables
        model_path = "models/yolov8n-face.pt"
        self.model = YOLO(model_path)

        self.cv_bridge = CvBridge()

    def camera_callback(self, msg):

        if self.use_compressed:
            image = self.cv_bridge.compressed_imgmsg_to_cv2(
                msg, desired_encoding="rgb8"
            )
        else:
            image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")

        results = self.model.predict(source=image, show=False)
        annotated = results[0].plot(show=False)

        if len(results[0].boxes.xywh.tolist()) != 0:  # Ensure detection

            # Get largest detection (closest face)
            largest_size = 0
            box = None
            for result in results:
                _, _, w, h = result.boxes.xywh.tolist()[0]
                size = w * h

                if size > largest_size:
                    largest_size = size
                    box = result.boxes.xywh.tolist()[0]

            # Create bounding box message
            box_msg = BoundingBox2D(
                center=Pose2D(
                    position=Point2D(x=box[0], y=box[1]),
                    theta=0.0,
                ),
                size_x=box[2],
                size_y=box[3],
            )

            # Publish bounding box
            self.publisher_bounding_box.publish(box_msg)

        # Publish annotated image
        self.publisher_annotation.publish(
            self.cv_bridge.cv2_to_imgmsg(annotated, encoding="rgb8")
        )


def main(args=None):
    rclpy.init(args=args)

    face_detection_node = FaceDetectionNode()

    rclpy.spin(face_detection_node)
    face_detection_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()