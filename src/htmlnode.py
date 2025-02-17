class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
                return self.value

        if self.children:
                children_html = ""
                for child in self.children:
                        children_html += child.to_html()
                return f"<{self.tag}>{children_html}</{self.tag}>"
        
        return f"<{self.tag}>{self.value or ''}</{self.tag}>"
        
    def props_to_html(self):
            result = ""
            if self.props == None:
                  return ""
            for key in self.props:
                result += f' {key}="{self.props[key]}"'
            return result
        
    def __repr__(self):
            return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def __eq__(self, other_node):
            if not isinstance(other_node, HTMLNode):
                  return False
            
            return self.tag == other_node.tag and self.value == other_node.value and self.children == other_node.children and self.props == other_node.props
                
                

class LeafNode(HTMLNode):
        def __init__(self, tag, value, props=None):
              super().__init__(tag, value, None, props)
              self.value = value
              self.tag = tag
              self.props = props


        def to_html(self):
                if self.value == None:
                        raise ValueError
                if self.tag == None:
                        return self.value
                if self.props == None:
                        return f"<{self.tag}>{self.value}</{self.tag}>"
                else:
                        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        def __repr__(self):
                return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
        def __init__(self, tag, children, props=None):
              super().__init__(tag, None, children, props)
        
        def to_html(self):
                if self.tag == None:
                      raise ValueError("Parent node must have HTML tag")
                if self.children == None:
                      raise ValueError("Parent node must have children")
                final_result = ""
                for child in self.children:
                      final_result += child.to_html()
                return f"<{self.tag}>{final_result}</{self.tag}>"
        
        def __repr__(self):
                return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

               


                   
               


        
        
                
